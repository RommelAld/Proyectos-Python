
import json
import time

import network
import ssd1306
from machine import I2C, PWM, Pin, time_pulse_us, unique_id
from umqtt.simple import MQTTClient

# ---------- CONFIGURACIÓN ----------
WIFI_SSID = "Wokwi-GUEST"        # red WiFi simulada de Wokwi (sin contraseña)
WIFI_PASS = ""
BROKER = "broker.hivemq.com"
PUERTO = 1883
TEMA = "contenedor-rommel-k7x2/datos"           # debe ser igual al TEMA del dashboard
TEMA_CMD = "contenedor-rommel-k7x2/comandos"    # debe ser igual al TEMA_CMD del dashboard
ALTURA_CM = 103                  # distancia del sensor con el contenedor vacío
LLENO_CM = 5                     # distancia del sensor con el contenedor lleno
UMBRAL_ALERTA = 80               # % desde el cual se enciende el LED verde
PERIODO_S = 2                    # segundos entre publicaciones

ID = "lixeira-" + "".join("{:02x}".format(b) for b in unique_id()[-3:])

# ---------- HARDWARE ----------
trig = Pin(32, Pin.OUT)
echo = Pin(27, Pin.IN)
led_rojo = Pin(2, Pin.OUT)
led_verde = Pin(4, Pin.OUT)
servo = PWM(Pin(17), freq=50)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---------- ESTADO ----------
aperturas = 0            # contador acumulado de aperturas de la tapa
pendiente_abrir = False  # lo activa el comando MQTT; se atiende en el bucle
cliente = None
estado_red = "conectando"


def mover_servo(grados):
    """Pulso de 0,5 ms (0°) a 2,5 ms (180°) sobre un periodo de 20 ms."""
    us = 500 + grados * 2000 // 180
    servo.duty_u16(us * 65535 // 20000)


def abrir_tapa():
    """Abre la tapa 2 s, la cierra y suma una apertura."""
    global aperturas
    mostrar(["Lixeira", "Abriendo tapa..."])
    mover_servo(90)
    time.sleep(2)
    mover_servo(0)
    aperturas += 1


# ---------- MEDICIÓN ----------
def medir_cm():
    """Una lectura del HC-SR04 en cm, o None si no hay eco."""
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)  # microsegundos; negativo si hay timeout
    if t < 0:
        return None
    return t / 58


def distancia_mediana(n=5):
    """Mediana de n lecturas, para descartar valores erráticos."""
    lecturas = []
    for _ in range(n):
        d = medir_cm()
        if d is not None:
            lecturas.append(d)
        time.sleep_ms(60)
    if not lecturas:
        return None
    lecturas.sort()
    return lecturas[len(lecturas) // 2]


def porcentaje(d):
    """0 % con ALTURA_CM (vacío), 100 % con LLENO_CM (lleno o desbordado)."""
    p = (ALTURA_CM - d) / (ALTURA_CM - LLENO_CM) * 100
    return max(0, min(100, p))


def nivel_texto(p):
    if p < 5:
        return "vazia"
    if p < UMBRAL_ALERTA:
        return "media"
    return "cheia"


# ---------- SALIDAS ----------
def actualizar_leds(p):
    verde = p >= UMBRAL_ALERTA
    led_verde.value(1 if verde else 0)
    led_rojo.value(0 if verde else 1)


def mostrar(lineas):
    oled.fill(0)
    for i, texto in enumerate(lineas):
        oled.text(texto, 0, i * 12)
    oled.show()


# ---------- RED ----------
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        inicio = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), inicio) > 15000:
                raise OSError("sin WiFi")
            time.sleep_ms(200)
    return wlan


def rssi(wlan):
    try:
        return wlan.status("rssi")
    except Exception:
        return None


def al_recibir(topic, msg):
    """Se ejecuta al llegar un mensaje en TEMA_CMD. Solo marca la orden."""
    global pendiente_abrir
    try:
        orden = json.loads(msg.decode())
    except ValueError:
        return
    if isinstance(orden, dict) and orden.get("cmd") == "abrir":
        pendiente_abrir = True


def conectar_mqtt():
    c = MQTTClient(ID, BROKER, PUERTO, keepalive=30)
    c.set_callback(al_recibir)
    c.connect()
    c.subscribe(TEMA_CMD)
    return c


def publicar(d, p):
    """Publica la lectura actual. Si falla algo, reintenta en el próximo ciclo."""
    global cliente, estado_red
    try:
        wlan = conectar_wifi()
        if cliente is None:
            cliente = conectar_mqtt()
        mensaje = json.dumps({
            "id": ID,
            "distancia_cm": round(d, 1),
            "ocupacao_pct": round(p, 1),
            "nivel": nivel_texto(p),
            "aperturas": aperturas,
            "rssi": rssi(wlan),
        })
        cliente.publish(TEMA, mensaje)
        estado_red = "MQTT ok"
        print(mensaje)
    except Exception as e:
        cliente = None
        estado_red = "sin conexion"
        print("Error de red:", e)


def esperar(segundos):
    """Espera atendiendo comandos. Si abre la tapa, vuelve antes para
    medir y publicar de inmediato el nuevo contador."""
    global cliente, pendiente_abrir
    fin = time.ticks_add(time.ticks_ms(), segundos * 1000)
    while time.ticks_diff(fin, time.ticks_ms()) > 0:
        if cliente is not None:
            try:
                cliente.check_msg()  # no bloquea; llama a al_recibir si hay mensaje
            except Exception:
                cliente = None
        if pendiente_abrir:
            pendiente_abrir = False
            abrir_tapa()
            return
        time.sleep_ms(100)


# ---------- PROGRAMA PRINCIPAL ----------
mover_servo(0)  # tapa cerrada

while True:
    d = distancia_mediana()
    if d is None:
        led_rojo.value(0)
        led_verde.value(0)
        mostrar(["Lixeira", "Sensor sin eco", "Revisar TRIG/ECHO"])
        esperar(PERIODO_S)
        continue

    p = porcentaje(d)
    actualizar_leds(p)
    publicar(d, p)
    mostrar([
        "Lixeira",
        "Nivel: {}%".format(round(p)),
        "Dist: {} cm".format(round(d)),
        "LED: " + ("verde" if p >= UMBRAL_ALERTA else "rojo"),
        "Aperturas: {}".format(aperturas),
        estado_red,
    ])
    esperar(PERIODO_S)
