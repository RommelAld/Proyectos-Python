
# Verificador simple de contraseñas.
# Rommel Aldana.
# Determina de manera simple si es una contraseña simple o dificil.


comunes = ["123456", "12345678", "123456789", "password", "qwerty",
           "abc123", "111111", "admin", "letmein", "iloveyou", "contraseña"]

# Caracteres que se cuentan como "especiales"
simbolos = "!@#$%^&*()-_=+[]{};:,.<>?/"

print("=== Verificador de contraseñas ===")
print("Escribe una contraseña. No uses contraseñas reales.")
print("Para terminar y salir de aca, escribe 'salir' ")

while True:
    clave = input("\nIngrese una Contraseña: ")

    if clave == "salir":
        print("Programa terminado, Gracias por Entrar.")
        break

    elif clave == "":
        print("No escribiste nada, Intenta de nuevo o si deseas salir, escribe 'salir' ")

    else:
        # tipos de caracteres de la contraseña
        mayusculas = 0
        minusculas = 0
        numeros = 0
        especiales = 0

        for caracter in clave:
            if caracter.isupper():
                mayusculas += 1
            elif caracter.islower():
                minusculas += 1
            elif caracter.isdigit():
                numeros += 1
            elif caracter in simbolos:
                especiales += 1

        #  Suma de los puntos y dar un consejo como lista
        puntos = 0
        consejos = []

        if len(clave) >= 12:
            puntos += 2
        elif len(clave) >= 8:
            puntos += 1
            consejos.append("Usa 12 caracteres o más.")
        else:
            consejos.append("Usa al menos 8 caracteres (mejor 12 o más).")


        if mayusculas > 0:
            puntos += 1
        else:
            consejos.append("Agrega letras mayúsculas.")
        if minusculas > 0:
            puntos += 1
        else:
            consejos.append("Agrega letras minúsculas.")


        if numeros > 0:
            puntos += 1
        else:
            consejos.append("Agrega números.")

        if especiales > 0:
            puntos += 1
        else:
            consejos.append("Agrega símbolos como ! # $ %.")

        # es una contraseña contraseña muy común?
        if clave.lower() in comunes:
            puntos = 0
            consejos.append("Es una contraseña muy común: un diccionario la encontraría en segundos.")

        # nivel según los puntos
        if puntos <= 2:
            nivel = "DÉBIL"
        elif puntos <= 4:
            nivel = "MEDIA"
        elif puntos == 5:
            nivel = "FUERTE"
        else:
            nivel = "MUY FUERTE"

         # hay 3 o más caracteres iguales seguidos como aaa, 111 etc.
        for i in range(len(clave) - 2):
            if clave[i] == clave[i + 1] and clave[i] == clave[i + 2]:
                puntos -= 1
                consejos.append("Evita repetir el mismo caracter 3 veces seguidas.")
                break

        # hay secuencias de 3 caracteres seguidos como abc, 123, qwe etc.
        filas = ["abcdefghijklmnopqrstuvwxyz", "0123456789",
                 "qwertyuiop", "asdfghjkl", "zxcvbnm"]
        minuscula = clave.lower()
        hay_secuencia = False

        for i in range(len(minuscula) - 2):
            trio = minuscula[i:i + 3]
            for fila in filas:
                if trio in fila or trio in fila[::-1]:
                    hay_secuencia = True

        if hay_secuencia:
            puntos -= 1
            consejos.append("Evita secuencias como abc, 123 o qwe.")

        # para que los puntos no bajen de 0
        if puntos < 0:
            puntos = 0

        # Mostrar el resultado
        print("\n--- Resultado ---")
        print("Largo:", len(clave))
        print("Mayúsculas:", mayusculas, "| Minúsculas:", minusculas,"| Números:", numeros, "| Símbolos:", especiales)
        print("Puntos en total:", puntos, "de 6")
        print("Nivel de seguridad:", nivel)

        if len(consejos) > 0:
            print("Consejos:")
            for consejo in consejos:
                print(" -", consejo)
