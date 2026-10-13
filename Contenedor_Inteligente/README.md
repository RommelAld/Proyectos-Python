# 🗑️ Contenedor inteligente

Proyecto colaborativo con un equipo de Brasil: un contenedor que mide **cuán lleno está** y envía los datos en formato **JSON** a un **dashboard web**.

El prototipo se construye en cartón y el funcionamiento es simulado (sin agua real). El sistema funcionaría igual en un contenedor real hecho con materiales más resistentes.

## Integrantes

- [completar con los nombres del equipo]

## Cómo funciona

```
HC-SR04 mide la distancia  →  ESP32 calcula el % de llenado
        →  enciende un LED (rojo o verde)
        →  publica un JSON por MQTT
        →  el dashboard lo recibe y lo muestra
```

## Componentes

| Componente | Función |
|---|---|
| ESP32 | Cerebro del sistema, con WiFi para enviar los datos |
| Sensor HC-SR04 | Va en la tapa y mide la distancia hasta el contenido |
| LED rojo | Le falta llenado |
| LED verde | Casi lleno o lleno |
| Servo | Apertura de la tapa |

## Lógica de los LEDs

- 🔴 **Rojo:** ocupación menor al 80 %.
- 🟢 **Verde:** ocupación de 80 % o más.

## Datos (JSON)

El ESP32 publica un JSON con el nivel de llenado y otros datos. La lista completa de campos, tipos y unidades está en [`campos_json.md`](campos_json.md).

## Dashboard

Muestra solo datos que se pueden obtener con los sensores del circuito:

- Medidor del nivel de llenado (%) y estado de los LEDs.
- Estado del dispositivo (en línea o sin señal).
- KPIs: **desbordes**, **tiempo medio de atención**, **aperturas del día** y **vaciados innecesarios**.
- Gráfico con el historial de llenado.

🔗 Dashboard en línea: [completar con el enlace de Streamlit]

## Simulación

🔗 Circuito en Wokwi: [completar con el enlace de la simulación]

![Circuito del proyecto](circuito.jpg)

## Cómo correr el dashboard en tu computador

1. Instalar Python 3.9 o más nuevo.
2. Instalar las librerías: `pip install -r requirements.txt`
3. Ejecutar: `streamlit run dashboard.py`
4. En la barra lateral, elegir **Simulación** (datos de prueba) o **MQTT** (datos reales del ESP32).

## Archivos

| Archivo | Contenido |
|---|---|
| `dashboard.py` | Dashboard hecho con Streamlit |
| `requirements.txt` | Librerías que necesita el dashboard |
| `campos_json.md` | Campos del JSON acordados con el equipo |
| `circuito.jpg` | Foto del circuito |
