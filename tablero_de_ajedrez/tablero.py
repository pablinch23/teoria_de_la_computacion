import tkinter as tk         # Importa Tkinter para crear interfaces gráficas
import csv                   # Para leer archivos CSV con las rutas
import ast                   # Para convertir strings tipo lista en estructuras reales

def leer_fila_csv(ruta_archivo, index):
    with open(ruta_archivo, 'r', newline='') as archivo:
        lector_csv = csv.reader(archivo)
        filas = list(lector_csv)                      # Convierte el CSV a una lista de filas
        if len(filas) == 0:                           # Verifica si el archivo está vacío
            print(f"El archivo {ruta_archivo} está vacío.")
            return None
        if index < 0 or index >= len(filas):          # Verifica que el índice esté dentro del rango
            raise IndexError("El índice está fuera de rango.")
        fila = ast.literal_eval(filas[index][0])      # Convierte la string de lista a lista real
        return fila

def posicion_a_fila_columna(pos):
    fila = (pos - 1) // 4                             # División entera para fila
    columna = (pos - 1) % 4                           # Resto para columna
    return fila, columna

def verificar_colision(pos1, pos2):
    return pos1 == pos2                               # Devuelve True si las posiciones son iguales

def Tablero(mov_1, mov_2, turno_i, tiempo=1000):
    ventana = tk.Tk()                                 # Crea una ventana
    ventana.title("Tablero Ajedrez (4x4)")            # Título de la ventana

    tablero = []
    for fila in range(4):
        fila_tablero = []
        for columna in range(4):
            color = 'white' if (fila + columna) % 2 == 0 else 'black'   # Color en patrón ajedrez
            casilla = tk.Label(ventana, bg=color, width=16, height=7,
                               borderwidth=1, relief="solid")           # Casilla del tablero
            casilla.grid(row=fila, column=columna, padx=1, pady=1)      # Ubicación en la cuadrícula
            fila_tablero.append(casilla)
        tablero.append(fila_tablero)

    movimientos_pieza1 = leer_fila_csv(mov_1, 0)      # Carga primera ruta de pieza 1
    movimientos_pieza2 = leer_fila_csv(mov_2, 0)      # Carga primera ruta de pieza 2

    if movimientos_pieza1 is None or movimientos_pieza2 is None:
        print("No se pudieron cargar los movimientos porque uno de los archivos CSV está vacío.")
        ventana.mainloop()
        return

    img_pieza1 = tk.PhotoImage(file="pieza1.png")     # Imagen de pieza 1
    img_pieza2 = tk.PhotoImage(file="pieza2.png")     # Imagen de pieza 2

    pos_pieza1 = movimientos_pieza1[0]                # Posición inicial de pieza 1
    pos_pieza2 = movimientos_pieza2[0]                # Posición inicial de pieza 2

    pieza1 = tk.Label(ventana, image=img_pieza1, width=80, height=80)
    pieza2 = tk.Label(ventana, image=img_pieza2, width=80, height=80)

    fila1, col1 = posicion_a_fila_columna(pos_pieza1)
    fila2, col2 = posicion_a_fila_columna(pos_pieza2)
    pieza1.grid(row=fila1, column=col1)
    pieza2.grid(row=fila2, column=col2)

    def mover_piezas(index_movimiento, index_ruta1, index_ruta2, turno, turnoinicial):
        nonlocal pos_pieza1, pos_pieza2, movimientos_pieza1, movimientos_pieza2

        # Si es el turno de la pieza 1
        if turno == 1:
            if index_movimiento < len(movimientos_pieza1):
                nueva_pos_pieza1 = movimientos_pieza1[index_movimiento]
                
                # Si hay colisión, se busca otra ruta
                while verificar_colision(nueva_pos_pieza1, pos_pieza2):
                    try:
                        index_ruta1 += 1
                        posible_ruta = leer_fila_csv("rutas/rutas_1.csv", index_ruta1)
                        if posible_ruta and posible_ruta[index_movimiento-1] == pos_pieza1:
                            print(f"Colisión de pieza 1 con la pieza 2 en posición: {pos_pieza2}")
                            movimientos_pieza1 = posible_ruta
                            nueva_pos_pieza1 = movimientos_pieza1[index_movimiento]
                            print(f"Nueva ruta de pieza 1: {movimientos_pieza1}")
                    except IndexError:
                        print("No se encontraron rutas adicionales para pieza 1, se saltará su turno.")
                        ventana.after(tiempo, mover_piezas, index_movimiento+1, index_ruta1, index_ruta2, 2, turnoinicial)
                        return

                pos_pieza1 = nueva_pos_pieza1
                if pos_pieza1 == 16 and index_movimiento == len(movimientos_pieza1)-1:
                    print("Pieza 1 llegó a la meta")

                fila, columna = posicion_a_fila_columna(pos_pieza1)
                pieza1.grid(row=fila, column=columna)

                # Alternar turno
                if turnoinicial == 1:
                    ventana.after(tiempo, mover_piezas, index_movimiento, index_ruta1, index_ruta2, 2, turnoinicial)
                else:
                    ventana.after(tiempo, mover_piezas, index_movimiento+1, index_ruta1, index_ruta2, 2, turnoinicial)
            else:
                print("Cadena terminada para pieza 1.")
                return

        elif turno == 2:
            if index_movimiento < len(movimientos_pieza2):
                nueva_pos_pieza2 = movimientos_pieza2[index_movimiento]
                while verificar_colision(nueva_pos_pieza2, pos_pieza1):
                    try:
                        index_ruta2 += 1
                        posible_ruta = leer_fila_csv("rutas/rutas_2.csv", index_ruta2)
                        if posible_ruta and posible_ruta[index_movimiento-1] == pos_pieza2:
                            print(f"Colisión de pieza 2 con la pieza 1 en posición: {pos_pieza1}")
                            movimientos_pieza2 = posible_ruta
                            nueva_pos_pieza2 = movimientos_pieza2[index_movimiento]
                            print(f"Nueva ruta de pieza 2: {movimientos_pieza2}")
                    except IndexError:
                        print("No se encontraron rutas adicionales para pieza 2, se saltará su turno.")
                        ventana.after(tiempo, mover_piezas, index_movimiento+1, index_ruta1, index_ruta2, 1, turnoinicial)
                        return
                pos_pieza2 = nueva_pos_pieza2
                if pos_pieza2 == 13 and index_movimiento == len(movimientos_pieza2)-1:
                    print("Pieza 2 llegó a la meta")
                fila, columna = posicion_a_fila_columna(pos_pieza2)
                pieza2.grid(row=fila, column=columna)

                if turnoinicial == 1:
                    ventana.after(tiempo, mover_piezas, index_movimiento+1, index_ruta1, index_ruta2, 1, turnoinicial)
                else:
                    ventana.after(tiempo, mover_piezas, index_movimiento, index_ruta1, index_ruta2, 1, turnoinicial)
            else:
                print("Cadena terminada para pieza 2.")
                return

    mover_piezas(1, 0, 0, turno_i, turno_i)       # Comienza desde la segunda posición (índice 1)
    ventana.mainloop()                           # Ejecuta la ventana gráfica

