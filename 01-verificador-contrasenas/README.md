# Verificador de contraseñas

Programa en Python que pide una contraseña por teclado, la analiza y dice qué tan segura es, con consejos para mejorarla. Lo hice para practicar cadenas, listas y ciclos, y para relacionarlo 

## ¿Cómo se puede ejecutar?

Necesitas tener Python 3 instalado en el Dispositivo, haciendo diferencia para macOS/Linux con Windows (Se puede ejecutar en la Terminal sin ningun Problema, claro con el Pyton Instalado).

```bash
# macOS / Linux
python3 verificador.py

# Windows
python verificador.py
```

Se debe escribr una contraseña de prueba y luego presionar Enter. Para terminar el programa debe escribir `salir`.

> **Importante:** Se debe usar solo una contraseña de prueba, nunca las contraseñas reales por motivos de Privacidad. El programa no guarda nada, pero es una buena costumbre que aprendi en varios cursos de Ciberseguridad.

## Ejemplo de ejecución

```text
Contraseña: MiPerro2020

--- Resultado ---
Largo: 11
Mayúsculas: 2 | Minúsculas: 5 | Números: 4 | Símbolos: 0
Puntos: 4 de 6
Nivel: MEDIA
Consejos:
 - Usa 12 caracteres o más.
 - Agrega símbolos (por ejemplo ! # $ %).

Contraseña: 123456

--- Resultado ---
Largo: 6
Mayúsculas: 0 | Minúsculas: 0 | Números: 6 | Símbolos: 0
Puntos: 0 de 6
Nivel: DÉBIL
Consejos:
 - Usa al menos 8 caracteres (mejor 12 o más).
 - Agrega letras mayúsculas.
 - Agrega letras minúsculas.
 - Agrega símbolos (por ejemplo ! # $ %).
 - Es una contraseña muy común: un diccionario la encontraría en segundos.
 - Evita secuencias como abc, 123 o qwe.
```

[Captura del programa](captura.png)

## Cómo funciona el Programa:

1. Recorre la contraseña con un `for` y cuenta mayúsculas, minúsculas, números y símbolos.
2. Suma puntos con un máximo de 6 según el largo y los tipos de caracteres que tiene.
3. Revisa si está en una lista de contraseñas muy comunes o en otras palabras wordlist; si lo está, los puntos bajan a 0.
4. Según los puntos, clasifica la contraseña como DÉBIL, MEDIA, FUERTE o MUY FUERTE.
5. Muestra el resultado y una lista de consejos para mejorarla.

## Conceptos de Python que practiqué

Como tal use comandos relativamente basicos, porque este prototipo fue solo por recreacion y mantener mis estudios vivos aun.

`input`, `print`, `while`, `for`, `if / elif / else`, listas (`append`), cadenas y sus métodos (`isupper`, `islower`, `isdigit`, `lower`), `len` y el operador `in`.

## Limitaciones que veo

Este verificador como tal es solo un ejercicio y no reemplaza a una herramienta profesional, hecha en linux por ejemplo, por los siguientes motivos:

- Solo mide el largo y los tipos de caracteres. Una contraseña como `MiPerro2020!!` sale "MUY FUERTE", pero es fácil de adivinar porque sigue un patrón común (nombre + año + símbolos).
- Y por Ultimo la lista de contraseñas comunes que use tiene solo 11 claves; los diccionarios reales que he probado como `rockyou.txt`, tienen millones.

## Ideas para mejorarlo

- Usar `getpass` para que la contraseña no se vea al escribirla.
- Leer la lista de contraseñas comunes desde un archivo.
- Pasar el código a funciones para que sea más ordenado.

## Qué aprendí

Lo más difícil fue el bloque que detecta 3 caracteres seguidos, porque usa cosas que no vi como tal en el liceo y tuve que analizarlo con pensamiento crítico para entender cómo funciona e investigarlo.

Lo pude relacionar con algunos proyectos de ciberseguridad de mi liceo, y con mis cursos de Cisco en ciberseguridad y Python.

También noté que, aunque el código no es tan complejo, sin la ayuda de la IA me habría costado, no por los comandos sino por lo extenso que era. Aun así, creo que se puede mejorar y comprimir más.

Lo próximo que quiero mejorar es optimizar mi trabajo junto a la IA: aprender a escribir código más corto y ordenado, por ejemplo usando funciones.
---

*Nota: este proyecto lo desarrollé con ayuda de IA (Claude) como herramienta de optimizacion, desarrollo y revisión; realize y probé el código yo mismo.*
