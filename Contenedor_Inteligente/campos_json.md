# Campos del JSON

Lista de los datos que publica el ESP32. **Los nombres y unidades deben ser iguales en los dos equipos**, o el dashboard no mostrará nada.

## Campos

| Campo | Tipo | Unidad / valores | ¿Lo usa el dashboard? |
|---|---|---|---|
| `id` | texto | Identificador del contenedor (ej. `lixeira-c40a24`) | Opcional |
| `distancia_cm` | número | Centímetros entre el sensor y el contenido | Opcional |
| `ocupacion_pct` | número | Porcentaje de llenado. Un valor de 100 o más significa **desborde** | **Obligatorio** |
| `nivel` | texto | Etiqueta del estado (ej. `vacia`, `media`, `llena`) | No |
| `aperturas` | entero | Contador **acumulado** de aperturas de la tapa | Opcional (para "Aperturas hoy") |
| `timestamp` | texto | Fecha y hora en formato ISO 8601 (ej. `2026-10-12T14:30:00`) | No (usa la hora de llegada) |

## Cómo se calcula el porcentaje

```
ocupacion_pct = (ALTURA_CM - distancia_cm) / ALTURA_CM * 100
```

`ALTURA_CM` es la distancia que mide el sensor con el contenedor **vacío**.

## Ejemplo

```json
{
  "id": "lixeira-c40a24",
  "distancia_cm": 38,
  "ocupacion_pct": 63,
  "nivel": "media",
  "aperturas": 12,
  "timestamp": "2026-10-12T14:30:00"
}
```

## Pendiente de acordar con el equipo de Brasil

- [ ] Idioma de los nombres: la simulación actual usa `ocupacao_pct` (portugués). El dashboard acepta `ocupacao_pct` y `ocupacion_pct`, pero conviene elegir uno solo.
- [ ] Valores exactos del campo `nivel`.
- [ ] Tema MQTT y broker (ej. `lixeira-equipo-2026/datos`).
- [ ] Cada cuántos segundos se envía un dato.
