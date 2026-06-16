# Gestion de Datos de Paises en Python

Trabajo Practico Integrador de Programacion: sistema de consola para administrar informacion de paises usando Python, listas, diccionarios, funciones, archivos CSV, filtros, ordenamientos y estadisticas.

## Integrantes

-Micael Nicolas Curtosi

## Archivos del proyecto

- `main.py`: programa principal.
- `paises.csv`: dataset base con paises.
- `documentacion.md`: informe tecnico y academico en formato editable.



## Como ejecutar

1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:

```bash
python main.py
```

En Windows, si el comando anterior no funciona, probar:

```bash
py main.py
```

## Funcionalidades

- Listar paises cargados desde CSV.
- Agregar un pais validando que no existan campos vacios.
- Actualizar poblacion y superficie de un pais existente.
- Buscar paises por coincidencia parcial o exacta del nombre.
- Filtrar por continente.
- Filtrar por rango de poblacion.
- Filtrar por rango de superficie.
- Ordenar por nombre, poblacion o superficie, en forma ascendente o descendente.
- Mostrar estadisticas:
  - Pais con mayor poblacion.
  - Pais con menor poblacion.
  - Promedio de poblacion.
  - Promedio de superficie.
  - Cantidad de paises por continente.

## Formato del CSV

El archivo `paises.csv` debe respetar esta estructura:

```csv
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,America
Japon,125800000,377975,Asia
```

## Ejemplo de uso

```text
Gestion de datos de paises
1. Listar paises
2. Agregar pais
3. Actualizar poblacion y superficie
4. Buscar pais por nombre
5. Filtrar paises
6. Ordenar paises
7. Mostrar estadisticas
0. Salir
Opcion:
```

