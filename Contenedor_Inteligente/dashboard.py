"""Dashboard del contenedor inteligente (Streamlit) - tema oscuro.

Instalar:   pip install streamlit paho-mqtt plotly pandas
Ejecutar:   streamlit run dashboard.py

Tiene dos fuentes de datos (se elige en la barra lateral):
  - Simulación: genera lecturas falsas para probar el dashboard sin el ESP32.
  - MQTT: recibe el JSON real que publica el ESP32.
"""
import json
import random
from datetime import date, datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------- CONFIGURACIÓN (cambiar aquí) ----------
BROKER = "broker.hivemq.com"     # broker público gratuito
PUERTO = 1883
TEMA = "lixeira/datos"           # debe ser el mismo tema que usa el ESP32
ALTURA_CM = 103                  # distancia del sensor con el contenedor vacío
UMBRAL_ALERTA = 80               # % desde el cual está "casi lleno" (LED verde)
CAIDA_VACIADO = 20               # bajada de 20 puntos o más = lo vaciaron
VACIADO_INNECESARIO = 40         # vaciarlo con menos de 40 % = viaje innecesario
SEGUNDOS_SIN_SENAL = 15          # sin datos por más de esto = dispositivo caído

# Acepta nombres de campos en portugués o español
ALIAS = {"ocupacao_pct": "ocupacion_pct", "distancia": "distancia_cm"}

# ---------- COLORES ----------
TARJETA = "#151a33"
GRILLA = "#2a3055"
TEXTO = "#c9cdea"
MORADO = "#c850f0"
CIAN = "#1de9e1"
AZUL = "#3b82f6"
LINEA = "#5aa9f0"
GRIS = "#2a3055"

st.set_page_config(page_title="Contenedor inteligente", page_icon="🗑️", layout="wide")

ESTILO = """
<style>
.stApp {background:#0f1226; color:#e8eaff;}
header[data-testid="stHeader"] {background:transparent;}
[data-testid="stSidebar"] {background:#12172e;}
.stApp [data-testid="stMarkdownContainer"] p, .stApp label, .stApp h1, .stApp h2, .stApp h3 {color:#e8eaff;}
[data-testid="stExpander"] {background:#151a33; border:none; border-radius:14px;}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary p {color:#e8eaff;}
div[data-testid="stPlotlyChart"], .stPlotlyChart {background:#151a33; border-radius:18px; padding:6px; overflow:hidden;}
.tarjeta {border-radius:18px; padding:18px 22px; height:210px; color:#fff; box-sizing:border-box;}
.morada {background:linear-gradient(135deg,#d96cf5,#8f6bff);}
.cian {background:linear-gradient(135deg,#1de9e1,#3b82f6);}
.t-titulo {font-size:15px; opacity:.92;}
.t-valor {font-size:44px; font-weight:700; line-height:1.15; margin-top:8px;}
.t-valor span {font-size:16px; font-weight:400; margin:0 10px 0 4px; opacity:.85;}
.t-sub {font-size:12px; opacity:.85; margin-top:8px;}
.barra {height:8px; background:rgba(255,255,255,.3); border-radius:6px; margin-top:12px;}
.barra div {height:8px; background:#fff; border-radius:6px;}
.fila {display:flex; align-items:center; background:#151a33; border-radius:16px; padding:7px 14px; margin-bottom:8px;}
.fila .ico {width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,#f06bb5,#a56bff); margin-right:12px; font-size:14px;}
.fila .nom {flex:1; font-size:14px; color:#e8eaff;}
.pill {padding:3px 12px; border-radius:10px; font-size:13px; background:#1d5a66; color:#7ff3ee;}
.pill.rojo {background:#5a2b4a; color:#ff9ac9;}
</style>
"""


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


# ---------- CÁLCULOS (KPIs y series) ----------
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


def aperturas_por_tiempo(df):
    """Aperturas agrupadas por minuto (datos recientes) o por hora."""
    if "aperturas" not in df:
        return None
    d = df.copy()
    d["nuevas"] = d["aperturas"].diff().clip(lower=0).fillna(0)
    if d["hora"].iloc[-1] - d["hora"].iloc[0] < timedelta(hours=2):
        titulo, paso, formato, cuantos = "Aperturas por minuto", "min", "%H:%M", 10
    else:
        titulo, paso, formato, cuantos = "Aperturas por hora", "60min", "%H:00", 12
    d["bloque"] = d["hora"].dt.floor(paso)
    serie = d.groupby("bloque")["nuevas"].sum().tail(cuantos)
    return titulo, list(serie.index.strftime(formato)), [int(v) for v in serie.values]


def partes_tiempo(tiempos):
    """Tiempo medio de atención listo para la tarjeta (HTML)."""
    if not tiempos:
        return "—"
    seg = int((sum(tiempos, timedelta()) / len(tiempos)).total_seconds())
    return f"{seg // 60}<span>min</span>{seg % 60}<span>s</span>"


# ---------- GRÁFICOS ----------
def estilo(fig, titulo, alto=320):
    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b>", font=dict(size=15, color="#ffffff"), x=0.03),
        paper_bgcolor=TARJETA, plot_bgcolor=TARJETA,
        font=dict(color=TEXTO), height=alto,
        margin=dict(t=55, b=25, l=35, r=20),
    )
    return fig


def fig_historial(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["hora"], y=df["ocupacion_pct"], mode="lines",
        line=dict(color=LINEA, width=3, shape="spline"),
        fill="tozeroy", fillcolor="rgba(90,169,240,0.12)",
    ))
    fig.add_hline(y=UMBRAL_ALERTA, line_dash="dot", line_color=MORADO,
                  annotation_text="Umbral", annotation_font_color=MORADO)
    i = df["ocupacion_pct"].idxmax()
    x, y = df.loc[i, "hora"], float(df.loc[i, "ocupacion_pct"])
    fig.add_trace(go.Scatter(
        x=[x], y=[y], mode="markers",
        marker=dict(size=12, color=CIAN, line=dict(width=6, color="rgba(29,233,225,0.3)")),
    ))
    fig.add_annotation(x=x, y=y, text=f"Máx = {y:.0f}%", showarrow=True,
                       arrowhead=0, arrowcolor=MORADO, ax=0, ay=-38,
                       bgcolor=MORADO, font=dict(color="white", size=12), borderpad=4)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(gridcolor=GRILLA, zeroline=False)
    fig.update_yaxes(gridcolor=GRILLA, zeroline=False, range=[0, 118], title="%")
    return estilo(fig, "Historial de llenado")


def fig_aperturas(titulo, etiquetas, valores):
    fig = go.Figure(go.Bar(
        x=etiquetas, y=valores,
        marker=dict(color=valores, cmin=0, cmax=max(max(valores), 1),
                    colorscale=[[0, "#6a6bdc"], [1, "#12e5e5"]]),
    ))
    fig.update_xaxes(gridcolor=GRILLA, zeroline=False)
    fig.update_yaxes(gridcolor=GRILLA, zeroline=False)
    return estilo(fig, titulo)


def fig_dona(titulo, etiquetas, valores, colores, centro):
    if sum(valores) == 0:
        etiquetas, valores, colores = ["Sin datos"], [1], [GRIS]
        info = "none"
    else:
        info = "percent"
    fig = go.Figure(go.Pie(
        labels=etiquetas, values=valores, hole=0.65, sort=False,
        marker=dict(colors=colores, line=dict(color=TARJETA, width=3)),
        textinfo=info, textfont=dict(color="#0f1226"),
    ))
    fig.add_annotation(text=centro, x=0.5, y=0.5, showarrow=False,
                       font=dict(size=16, color="#ffffff"))
    fig.update_layout(legend=dict(font=dict(color=TEXTO)))
    return estilo(fig, titulo, alto=300)


# ---------- PIEZAS DE HTML ----------
def tarjeta(clase, titulo, valor_html, extra=""):
    return (f'<div class="tarjeta {clase}"><div class="t-titulo">{titulo}</div>'
            f'<div class="t-valor">{valor_html}</div>{extra}</div>')


def fila(icono, nombre, valor, rojo=False):
    clase = "pill rojo" if rojo else "pill"
    return (f'<div class="fila"><div class="ico">{icono}</div>'
            f'<div class="nom">{nombre}</div><div class="{clase}">{valor}</div></div>')


# ---------- DASHBOARD ----------
CFG = {"displayModeBar": False}


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
    en_linea = seg < SEGUNDOS_SIN_SENAL
    verde = p >= UMBRAL_ALERTA

    # Fila 1: tarjetas con degradado + indicadores
    a1, a2, a3 = st.columns([1, 1, 1.15])
    barra = f'<div class="barra"><div style="width:{min(p, 100):.0f}%"></div></div>'
    dist = f'<div class="t-sub">Distancia medida: {ultimo.get("distancia_cm", "—")} cm</div>'
    a1.markdown(
        tarjeta("morada", "Nivel de llenado", f'{p:.0f}<span>%</span>', barra + dist),
        unsafe_allow_html=True)
    a2.markdown(
        tarjeta("cian", "Tiempo medio de atención", partes_tiempo(tiempos),
                f'<div class="t-sub">Desde la alerta (≥{UMBRAL_ALERTA}%) hasta el vaciado</div>'),
        unsafe_allow_html=True)
    a3.markdown(
        fila("🚨", "Desbordes", desbordes, rojo=desbordes > 0)
        + fila("🚪", "Aperturas hoy", "—" if aper is None else aper)
        + fila("📡", "Dispositivo", "En línea" if en_linea else "Sin señal", rojo=not en_linea)
        + fila("💡", "LED encendido", "Verde" if verde else "Rojo", rojo=not verde),
        unsafe_allow_html=True)

    # Fila 2: historial + aperturas
    b1, b2 = st.columns([2, 1])
    b1.plotly_chart(fig_historial(df), config=CFG)
    serie = aperturas_por_tiempo(df)
    if serie:
        b2.plotly_chart(fig_aperturas(*serie), config=CFG)
    else:
        b2.info("El JSON no trae el contador «aperturas».")

    # Fila 3: donas
    n = len(df)
    bajo = int((df["ocupacion_pct"] < VACIADO_INNECESARIO).sum())
    alto = int((df["ocupacion_pct"] >= UMBRAL_ALERTA).sum())
    medio = n - bajo - alto
    c1, c2 = st.columns(2)
    c1.plotly_chart(fig_dona(
        "Tiempo en cada nivel",
        [f"Bajo (<{VACIADO_INNECESARIO}%)", "Medio", f"Alto (≥{UMBRAL_ALERTA}%)"],
        [bajo, medio, alto], [CIAN, AZUL, MORADO], f"{n}<br>lecturas"), config=CFG)
    c2.plotly_chart(fig_dona(
        "Vaciados necesarios vs innecesarios",
        ["Necesarios", "Innecesarios"],
        [vaciados - innecesarios, innecesarios], [CIAN, MORADO],
        f"Vaciados<br>{vaciados}"), config=CFG)

    with st.expander("Último JSON recibido"):
        st.json({k: str(v) for k, v in ultimo.to_dict().items()})


st.markdown(ESTILO, unsafe_allow_html=True)
st.markdown("## 🗑️ Contenedor inteligente")
fuente = st.sidebar.radio("Fuente de datos", ["Simulación", "MQTT"])
st.sidebar.caption(f"Broker: {BROKER}\n\nTema: {TEMA}")
tablero(fuente)
