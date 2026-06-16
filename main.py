import csv
from pathlib import Path


ARCHIVO_CSV = Path("paises.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]


def normalizar_texto(texto):
    return texto.strip()


def leer_entero(mensaje, minimo=None):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if minimo is not None and numero < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print("Ingrese un numero entero valido.")


def leer_texto(mensaje):
    while True:
        texto = normalizar_texto(input(mensaje))
        if texto:
            return texto
        print("El campo no puede estar vacio.")


def cargar_paises(ruta=ARCHIVO_CSV):
    paises = []
    if not ruta.exists():
        print("No se encontro el archivo CSV. Se iniciara una lista vacia.")
        return paises

    try:
        with ruta.open("r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if lector.fieldnames != CAMPOS:
                print("El CSV no tiene el formato esperado.")
                return paises

            for numero_linea, fila in enumerate(lector, start=2):
                try:
                    pais = {
                        "nombre": normalizar_texto(fila["nombre"]),
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": normalizar_texto(fila["continente"]),
                    }
                    if not pais["nombre"] or not pais["continente"]:
                        raise ValueError("campos de texto vacios")
                    if pais["poblacion"] <= 0 or pais["superficie"] <= 0:
                        raise ValueError("valores numericos no positivos")
                    paises.append(pais)
                except (ValueError, TypeError) as error:
                    print(f"Linea {numero_linea} ignorada por formato invalido: {error}")
    except OSError as error:
        print(f"No se pudo leer el archivo CSV: {error}")

    return paises


def guardar_paises(paises, ruta=ARCHIVO_CSV):
    try:
        with ruta.open("w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(paises)
    except OSError as error:
        print(f"No se pudo guardar el archivo CSV: {error}")


def mostrar_pais(pais):
    print(
        f"{pais['nombre']} | Poblacion: {pais['poblacion']} | "
        f"Superficie: {pais['superficie']} km2 | Continente: {pais['continente']}"
    )


def mostrar_lista(paises):
    if not paises:
        print("No hay paises para mostrar.")
        return

    for indice, pais in enumerate(paises, start=1):
        print(f"{indice}. ", end="")
        mostrar_pais(pais)


def existe_pais(paises, nombre):
    nombre_buscado = nombre.lower()
    return any(pais["nombre"].lower() == nombre_buscado for pais in paises)


def agregar_pais(paises):
    print("\nAgregar pais")
    nombre = leer_texto("Nombre: ")
    if existe_pais(paises, nombre):
        print("Ya existe un pais con ese nombre.")
        return

    poblacion = leer_entero("Poblacion: ", minimo=1)
    superficie = leer_entero("Superficie en km2: ", minimo=1)
    continente = leer_texto("Continente: ")

    paises.append(
        {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente,
        }
    )
    guardar_paises(paises)
    print("Pais agregado correctamente.")


def buscar_paises(paises):
    termino = leer_texto("Ingrese nombre o parte del nombre: ").lower()
    encontrados = [
        pais for pais in paises if termino in pais["nombre"].lower()
    ]
    mostrar_lista(encontrados)


def seleccionar_pais_por_nombre(paises):
    nombre = leer_texto("Nombre exacto del pais: ").lower()
    for pais in paises:
        if pais["nombre"].lower() == nombre:
            return pais
    return None


def actualizar_pais(paises):
    print("\nActualizar poblacion y superficie")
    pais = seleccionar_pais_por_nombre(paises)
    if pais is None:
        print("No se encontro un pais con ese nombre.")
        return

    mostrar_pais(pais)
    pais["poblacion"] = leer_entero("Nueva poblacion: ", minimo=1)
    pais["superficie"] = leer_entero("Nueva superficie en km2: ", minimo=1)
    guardar_paises(paises)
    print("Datos actualizados correctamente.")


def filtrar_por_continente(paises):
    continente = leer_texto("Continente: ").lower()
    resultado = [
        pais for pais in paises if pais["continente"].lower() == continente
    ]
    mostrar_lista(resultado)


def leer_rango(nombre_campo):
    minimo = leer_entero(f"{nombre_campo} minima: ", minimo=0)
    maximo = leer_entero(f"{nombre_campo} maxima: ", minimo=minimo)
    return minimo, maximo


def filtrar_por_rango(paises, campo):
    minimo, maximo = leer_rango(campo.capitalize())
    resultado = [
        pais for pais in paises if minimo <= pais[campo] <= maximo
    ]
    mostrar_lista(resultado)


def menu_filtros(paises):
    while True:
        print("\nFiltros")
        print("1. Por continente")
        print("2. Por rango de poblacion")
        print("3. Por rango de superficie")
        print("0. Volver")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            filtrar_por_continente(paises)
        elif opcion == "2":
            filtrar_por_rango(paises, "poblacion")
        elif opcion == "3":
            filtrar_por_rango(paises, "superficie")
        elif opcion == "0":
            return
        else:
            print("Opcion invalida.")


def ordenar_paises(paises):
    print("\nOrdenar paises")
    print("1. Nombre")
    print("2. Poblacion")
    print("3. Superficie")
    opcion_campo = input("Campo: ").strip()

    campos = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    campo = campos.get(opcion_campo)
    if campo is None:
        print("Campo invalido.")
        return

    print("1. Ascendente")
    print("2. Descendente")
    opcion_orden = input("Orden: ").strip()
    if opcion_orden not in ("1", "2"):
        print("Orden invalido.")
        return

    descendente = opcion_orden == "2"
    ordenados = sorted(paises, key=lambda pais: pais[campo], reverse=descendente)
    mostrar_lista(ordenados)


def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos para calcular estadisticas.")
        return

    mayor_poblacion = max(paises, key=lambda pais: pais["poblacion"])
    menor_poblacion = min(paises, key=lambda pais: pais["poblacion"])
    promedio_poblacion = sum(pais["poblacion"] for pais in paises) / len(paises)
    promedio_superficie = sum(pais["superficie"] for pais in paises) / len(paises)
    por_continente = {}

    for pais in paises:
        continente = pais["continente"]
        por_continente[continente] = por_continente.get(continente, 0) + 1

    print("\nEstadisticas")
    print("Pais con mayor poblacion:")
    mostrar_pais(mayor_poblacion)
    print("Pais con menor poblacion:")
    mostrar_pais(menor_poblacion)
    print(f"Promedio de poblacion: {promedio_poblacion:.2f}")
    print(f"Promedio de superficie: {promedio_superficie:.2f} km2")
    print("Cantidad de paises por continente:")
    for continente, cantidad in sorted(por_continente.items()):
        print(f"- {continente}: {cantidad}")


def mostrar_menu():
    print("\nGestion de datos de paises")
    print("1. Listar paises")
    print("2. Agregar pais")
    print("3. Actualizar poblacion y superficie")
    print("4. Buscar pais por nombre")
    print("5. Filtrar paises")
    print("6. Ordenar paises")
    print("7. Mostrar estadisticas")
    print("0. Salir")


def main():
    paises = cargar_paises()

    while True:
        mostrar_menu()
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            mostrar_lista(paises)
        elif opcion == "2":
            agregar_pais(paises)
        elif opcion == "3":
            actualizar_pais(paises)
        elif opcion == "4":
            buscar_paises(paises)
        elif opcion == "5":
            menu_filtros(paises)
        elif opcion == "6":
            ordenar_paises(paises)
        elif opcion == "7":
            mostrar_estadisticas(paises)
        elif opcion == "0":
            guardar_paises(paises)
            print("Programa finalizado.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
