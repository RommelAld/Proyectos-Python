import json
import random
from datetime import date, datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------- CONFIGURACIÓN (cambiar aquí) ----------
BROKER = "broker.hivemq.com"     # broker público gratuito
PUERTO = 1883
TEMA = "lixeira-rommel-2026/datos"           # debe ser el mismo tema que usa el ESP32
ALTURA_CM = 103                  # distancia del sensor con el contenedor vacío
UMBRAL_ALERTA = 80               # % desde el cual está "casi lleno" (LED verde)
CAIDA_VACIADO = 20               # bajada de 20 puntos o más = lo vaciaron
VACIADO_INNECESARIO = 40         # vaciarlo con menos de 40 % = viaje innecesario
SEGUNDOS_SIN_SENAL = 15          # sin datos por más de esto = dispositivo caído

# Acepta nombres de campos en portugués o español
ALIAS = {"ocupacao_pct": "ocupacion_pct", "distancia": "distancia_cm"}

st.set_page_config(page_title="Contenedor inteligente", page_icon="🗑️", layout="wide")


# ---------- FUENTES DE DATOS ----------
@st.cache_resource
def iniciar_mqtt():
    """Se conecta al broker una sola vez y va guardando los mensajes."""
    import paho.mqtt.client as mqtt

    mensajes = []

    def al_conectar(client, userdata, flags, rc, props=None):
        client.subscribe(TEMA)

    def al_recibir(client, userdata, msg):
        try:
            d = json.loads(msg.payload.decode())
            d = {ALIAS.get(k, k): v for k, v in d.items()}
            d["hora"] = datetime.now()
            mensajes.append(d)
            del mensajes[:-2000]  # limitar memoria
        except (ValueError, UnicodeDecodeError):
            pass

    cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    cliente.on_connect = al_conectar
    cliente.on_message = al_recibir
    cliente.connect(BROKER, PUERTO, 60)
    cliente.loop_start()
    return mensajes


def simular():
    """Agrega una lectura falsa cada vez que se llama."""
    if "sim" not in st.session_state:
        st.session_state.sim = {"pct": 10.0, "aperturas": 0, "datos": []}
    s = st.session_state.sim
    s["pct"] += random.uniform(2, 6)
    if s["pct"] >= 108 or random.random() < 0.03:
        s["pct"] = random.uniform(0, 8)  # lo vaciaron
    if random.random() < 0.5:
        s["aperturas"] += 1
    pct = round(min(s["pct"], 110), 1)
    s["datos"].append({
        "id": "lixeira-sim",
        "distancia_cm": round(max(0, ALTURA_CM * (1 - pct / 100)), 1),
        "ocupacion_pct": pct,
        "aperturas": s["aperturas"],
        "hora": datetime.now(),
    })
    del s["datos"][:-2000]
    return s["datos"]


# ---------- CÁLCULO DE KPIs ----------
def calcular_kpis(df):
    """Convierte las lecturas sueltas en números resumidos."""
    desbordes = vaciados = innecesarios = 0
    tiempos = []
    alerta_desde = None
    en_desborde = False
    anterior = None
    for _, f in df.iterrows():
        p = f["ocupacion_pct"]
        # Desborde: pasa del 100 % (se cuenta una vez por episodio)
        if p >= 100 and not en_desborde:
            desbordes += 1
        en_desborde = p >= 100
        # Vaciado: el nivel baja de golpe
        if anterior is not None and anterior - p >= CAIDA_VACIADO:
            vaciados += 1
            if anterior < VACIADO_INNECESARIO:
                innecesarios += 1
            if alerta_desde is not None:
                tiempos.append(f["hora"] - alerta_desde)
            alerta_desde = None
        # Inicio de la alerta (llegó al umbral)
        if p >= UMBRAL_ALERTA and alerta_desde is None:
            alerta_desde = f["hora"]
        anterior = p
    return desbordes, vaciados, innecesarios, tiempos


def aperturas_hoy(df):
    if "aperturas" not in df:
        return None
    hoy = df[df["hora"].dt.date == date.today()]
    return int(hoy["aperturas"].diff().clip(lower=0).sum())


def formato_tiempo(tiempos):
    if not tiempos:
        return "—"
    seg = (sum(tiempos, timedelta()) / len(tiempos)).total_seconds()
    return f"{int(seg // 60)} min {int(seg % 60)} s"


# ---------- DASHBOARD ----------
@st.fragment(run_every=2)
def tablero(fuente):
    if fuente == "Simulación":
        datos = simular()
    else:
        try:
            datos = iniciar_mqtt()
        except Exception as e:
            st.error(f"No se pudo conectar al broker MQTT: {e}")
            return
    if not datos:
        st.info(f"Esperando datos en el tema «{TEMA}»…")
        return

    df = pd.DataFrame(list(datos))
    if "ocupacion_pct" not in df:
        st.error("El JSON recibido no trae el campo «ocupacion_pct».")
        return

    ultimo = df.iloc[-1]
    p = float(ultimo["ocupacion_pct"])
    seg = (datetime.now() - ultimo["hora"]).total_seconds()
    desbordes, vaciados, innecesarios, tiempos = calcular_kpis(df)
    aper = aperturas_hoy(df)

    # Fila 1: medidor + estado
    c1, c2 = st.columns([2, 1])
    with c1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=min(p, 100),
            number={"suffix": " %"},
            title={"text": "Nivel de llenado"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2e7d32" if p >= UMBRAL_ALERTA else "#c62828"},
                "steps": [
                    {"range": [0, UMBRAL_ALERTA], "color": "#fdecea"},
                    {"range": [UMBRAL_ALERTA, 100], "color": "#e6f4ea"},
                ],
                "threshold": {"line": {"color": "black", "width": 3}, "value": UMBRAL_ALERTA},
            },
        ))
        fig.update_layout(height=280, margin=dict(t=50, b=0, l=20, r=20))
        st.plotly_chart(fig)
    with c2:
        st.subheader("Estado")
        if p >= UMBRAL_ALERTA:
            st.markdown("### 🟢 LED verde\nCasi lleno o lleno")
        else:
            st.markdown("### 🔴 LED rojo\nLe falta llenado")
        if seg < SEGUNDOS_SIN_SENAL:
            st.markdown(f"**Dispositivo:** 🟢 en línea (hace {int(seg)} s)")
        else:
            st.markdown("**Dispositivo:** 🔴 sin señal")
        st.caption(f"Distancia medida: {ultimo.get('distancia_cm', '—')} cm")

    # Fila 2: KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Desbordes", desbordes)
    k2.metric("Tiempo medio de atención", formato_tiempo(tiempos))
    k3.metric("Aperturas hoy", "—" if aper is None else aper)
    k4.metric("Vaciados innecesarios", f"{innecesarios} de {vaciados}")

    # Fila 3: historial
    linea = go.Figure(go.Scatter(x=df["hora"], y=df["ocupacion_pct"], mode="lines"))
    linea.add_hline(y=UMBRAL_ALERTA, line_dash="dash", annotation_text="Umbral")
    linea.update_layout(
        title="Historial de llenado",
        yaxis={"title": "%", "range": [0, 115]},
        height=320,
        margin=dict(t=50, b=20),
    )
    st.plotly_chart(linea)

    with st.expander("Último JSON recibido"):
        st.json({k: str(v) for k, v in ultimo.to_dict().items()})


st.title("🗑️ Contenedor inteligente")
fuente = st.sidebar.radio("Fuente de datos", ["Simulación", "MQTT"])
st.sidebar.caption(f"Broker: {BROKER}\n\nTema: {TEMA}")
tablero(fuente)
