import secrets
import string

def generar_contrasena(longitud=12):
    """Genera una contraseña segura de la longitud especificada."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena

def main():
    while True:
        try:
            longitud = int(input("Introduce la longitud deseada para la contraseña (mínimo 8): "))
            if longitud < 8:
                print("La longitud mínima es 8 caracteres. Por favor, inténtalo de nuevo.")
                continue
            break
        except ValueError:
            print("Por favor, introduce un número entero válido.")

    contrasena = generar_contrasena(longitud)
    print(f"Tu contraseña segura es: {contrasena}")

if __name__ == "__main__":
    main()
