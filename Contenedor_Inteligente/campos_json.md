{
  "version": 1,
  "author": "Uri Shaked",
  "editor": "wokwi",
  "parts": [
    {
      "type": "wokwi-breadboard-half",
      "id": "bb1",
      "top": 400.2,
      "left": -352.4,
      "attrs": {}
    },
    {
      "type": "board-esp32-devkit-c-v4",
      "id": "esp",
      "top": 288,
      "left": 43.24,
      "attrs": {
        "env": "micropython-20231005-v1.21.0"
      }
    },
    {
      "type": "board-ssd1306",
      "id": "oled1",
      "top": 358.34,
      "left": 249.83,
      "attrs": {}
    },
    {
      "type": "wokwi-hc-sr04",
      "id": "ultrasonic1",
      "top": 183.9,
      "left": -378.5,
      "attrs": {}
    },
    {
      "type": "wokwi-led",
      "id": "led1",
      "top": 418.8,
      "left": -274.6,
      "attrs": {
        "color": "red"
      }
    },
    {
      "type": "wokwi-led",
      "id": "led2",
      "top": 418.8,
      "left": -245.8,
      "attrs": {
        "color": "limegreen"
      }
    },
    {
      "type": "wokwi-servo",
      "id": "servo1",
      "top": 75.8,
      "left": -151.8,
      "rotate": 270,
      "attrs": {}
    },
    {
      "type": "wokwi-resistor",
      "id": "r1",
      "top": 494.4,
      "left": -288.55,
      "rotate": 90,
      "attrs": {
        "value": "220"
      }
    },
    {
      "type": "wokwi-resistor",
      "id": "r2",
      "top": 494.4,
      "left": -259.75,
      "rotate": 90,
      "attrs": {
        "value": "220"
      }
    },
    {
      "type": "wokwi-resistor",
      "id": "r3",
      "top": 484.8,
      "left": -211.75,
      "rotate": 90,
      "attrs": {
        "value": "1000"
      }
    },
    {
      "type": "wokwi-resistor",
      "id": "r4",
      "top": 561.6,
      "left": -211.75,
      "rotate": 90,
      "attrs": {
        "value": "2000"
      }
    }
  ],
  "connections": [
    [
      "esp:TX",
      "$serialMonitor:RX",
      "",
      []
    ],
    [
      "esp:RX",
      "$serialMonitor:TX",
      "",
      []
    ],
    [
      "oled1:SCL",
      "esp:22",
      "green",
      [
        "v0"
      ]
    ],
    [
      "oled1:SDA",
      "esp:21",
      "blue",
      [
        "v-19.2",
        "h-124.73"
      ]
    ],
    [
      "oled1:GND",
      "esp:GND.2",
      "black",
      [
        "v-67.2",
        "h-96"
      ]
    ],
    [
      "oled1:VCC",
      "esp:3V3",
      "red",
      [
        "v-28.8",
        "h0.15",
        "v-76.8",
        "h-201.75"
      ]
    ],
    [
      "ultrasonic1:VCC",
      "bb1:tp.3",
      "red",
      [
        "v0"
      ]
    ],
    [
      "ultrasonic1:GND",
      "bb1:tn.5",
      "black",
      [
        "v0"
      ]
    ],
    [
      "bb1:tp.1",
      "bb1:bp.1",
      "red",
      [
        "v-9.3",
        "h-75.2",
        "v172.8"
      ]
    ],
    [
      "bb1:tn.1",
      "bb1:bn.1",
      "black",
      [
        "v-0.1",
        "h-56",
        "v172.8"
      ]
    ],
    [
      "esp:2",
      "bb1:9t.c",
      "green",
      [
        "h67.2",
        "v192",
        "h-422.4"
      ]
    ],
    [
      "led2:A",
      "bb1:12t.b",
      "",
      [
        "$bb"
      ]
    ],
    [
      "led2:C",
      "bb1:11t.b",
      "",
      [
        "$bb"
      ]
    ],
    [
      "led1:A",
      "bb1:9t.b",
      "",
      [
        "$bb"
      ]
    ],
    [
      "led1:C",
      "bb1:8t.b",
      "",
      [
        "$bb"
      ]
    ],
    [
      "r1:1",
      "bb1:8t.c",
      "",
      [
        "$bb"
      ]
    ],
    [
      "r1:2",
      "bb1:8b.g",
      "",
      [
        "$bb"
      ]
    ],
    [
      "r2:1",
      "bb1:11t.c",
      "",
      [
        "$bb"
      ]
    ],
    [
      "r2:2",
      "bb1:11b.g",
      "",
      [
        "$bb"
      ]
    ],
    [
      "bb1:8b.j",
      "bb1:bn.6",
      "green",
      [
        "v0"
      ]
    ],
    [
      "bb1:11b.j",
      "bb1:bn.9",
      "green",
      [
        "v0"
      ]
    ],
    [
      "servo1:GND",
      "bb1:tn.15",
      "black",
      [
        "v124.8",
        "h-96"
      ]
    ],
    [
      "servo1:V+",
      "bb1:tp.16",
      "red",
      [
        "v172.8",
        "h-76.7"
      ]
    ],
    [
      "esp:17",
      "servo1:PWM",
      "yellow",
      [
        "h48",
        "v-172.8",
        "h-249.6"
      ]
    ],
    [
      "r3:1",
      "bb1:16t.b",
      "",
      [
        "$bb"
      ]
    ],
    [
      "r3:2",
      "bb1:16b.f",
      "",
      [
        "$bb"
      ]
    ],
    [
      "ultrasonic1:ECHO",
      "bb1:16t.a",
      "green",
      [
        "v57.6",
        "h85.6"
      ]
    ],
    [
      "r3:2",
      "r4:1",
      "green",
      [
        "h0"
      ]
    ],
    [
      "esp:27",
      "bb1:16b.g",
      "green",
      [
        "h-47.85",
        "v115.2"
      ]
    ],
    [
      "ultrasonic1:TRIG",
      "esp:32",
      "green",
      [
        "v96",
        "h28.4"
      ]
    ],
    [
      "r4:1",
      "bb1:16b.h",
      "",
      [
        "$bb"
      ]
    ],
    [
      "r4:2",
      "bb1:bn.13",
      "",
      [
        "$bb"
      ]
    ],
    [
      "esp:5V",
      "bb1:tp.2",
      "red",
      []
    ],
    [
      "esp:GND.1",
      "bb1:tn.2",
      "black",
      []
    ],
    [
      "esp:4",
      "bb1:12t.c",
      "limegreen",
      []
    ]
  ],
  "dependencies": {}
}
