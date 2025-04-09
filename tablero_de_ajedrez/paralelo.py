import numpy as np                     # Para manejar listas y generar aleatorios si se necesitara
import csv                             # Para leer y escribir archivos CSV
import networkx as nx                  # (No se usa aquí directamente, pero quizá estaba planeado)
import matplotlib.pyplot as plt        # (Tampoco se usa directamente en este script)

# Crea un tablero 4x4 numerado del 1 al 16
tablero = [[(i * 4) + j + 1 for j in range(4)] for i in range(4)]
# Resultado: [[1, 2, 3, 4], [5, 6, 7, 8], ..., [13, 14, 15, 16]]

# Una casilla es blanca si la suma de su fila + columna es par
def es_blanca(i, j):
    return (i + j) % 2 == 0

# Crea una matriz 4x4 con True (blanca) o False (negra) según cada posición
colores = [[es_blanca(i, j) for j in range(4)] for i in range(4)]

# Movimientos válidos (horizontal, vertical y diagonales)
movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0),
               (1, 1), (1, -1), (-1, 1), (-1, -1)]
def posicion_valida(i, j):
    return 0 <= i < 4 and 0 <= j < 4

def generar_transiciones():
    transiciones = {}
    for i in range(4):                            # Recorre filas
        for j in range(4):                        # Recorre columnas
            estado_actual = tablero[i][j]         # Obtiene el número de casilla
            transiciones[estado_actual] = {'w': [], 'b': []}  # Inicializa diccionario de movimientos
            
            for di, dj in movimientos:            # Aplica todos los movimientos posibles
                ni, nj = i + di, j + dj           # Nueva posición
                if posicion_valida(ni, nj):       # Si está dentro del tablero
                    siguiente_estado = tablero[ni][nj]  # Número de la nueva casilla
                    if colores[ni][nj]:                 # Si es blanca
                        transiciones[estado_actual]['w'].append(siguiente_estado)
                    else:
                        transiciones[estado_actual]['b'].append(siguiente_estado)
    return transiciones

def calcular_rutas_paralelo(cadena, q0, qf):
    transiciones = generar_transiciones()             # Diccionario con movimientos posibles
    estado_inicial = q0                               # Nodo inicial
    estado_final = qf                                 # Nodo objetivo

    estados_actuales = {(estado_inicial, tuple([estado_inicial]))}  # Ruta inicial: solo el estado inicial

    for simbolo in cadena:                            # Por cada símbolo en la cadena
        nuevos_estados = set()
        for estado, ruta in estados_actuales:         # Por cada estado actual y su ruta
            for siguiente in transiciones[estado][simbolo]:  # Transiciones válidas con ese símbolo
                nueva_ruta = ruta + (siguiente,)      # Añadir el nuevo estado a la ruta
                nuevos_estados.add((siguiente, nueva_ruta))
        estados_actuales = nuevos_estados             # Actualizar los estados actuales

    # Convertir rutas a listas
    todas_las_rutas = [list(ruta) for estado, ruta in estados_actuales]
    rutas_validas = [list(ruta) for estado, ruta in estados_actuales if estado == estado_final]
    return todas_las_rutas, rutas_validas

def guardar_rutas_en_csv(player, todas_las_rutas, rutas_validas):
    with open(f"rutas/rutas_posibles_{player}.csv", "w", newline="") as archivo_todas:
        escritor_csv = csv.writer(archivo_todas)
        for ruta in todas_las_rutas:
            escritor_csv.writerow([ruta])                  # Escribe todas las rutas

    with open(f"rutas/rutas_{player}.csv", "w", newline="") as archivo_validas:
        escritor_csv = csv.writer(archivo_validas)
        for ruta in rutas_validas:
            escritor_csv.writerow([ruta])                  # Escribe solo las válidas

def Generar_Rutas(cadena1, cadena2):
    # Pieza 1: inicia en casilla 1 (blanca) y termina en 16 (blanca)
    # Pieza 2: inicia en casilla 4 (negra) y termina en 13 (negra)
    rutas_pos_1, rutas_validas_1 = calcular_rutas_paralelo(cadena1, 1, 16)
    rutas_pos_2, rutas_validas_2 = calcular_rutas_paralelo(cadena2, 4, 13)

    guardar_rutas_en_csv(1, rutas_pos_1, rutas_validas_1)
    guardar_rutas_en_csv(2, rutas_pos_2, rutas_validas_2)

    print("Se han guardado todas las rutas en archivos CSV.")
