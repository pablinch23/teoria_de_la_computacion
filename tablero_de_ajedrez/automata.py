from tablero import Tablero                      # Importa la función para mostrar animación visual del tablero
from paralelo import Generar_Rutas               # Importa la función que genera rutas posibles y ganadoras
from grafo import graficarRutas                  # Importa la función para graficar las rutas como grafos
import numpy as np                               # Importa NumPy para generar números aleatorios y manejar arrays

# Menú principal del sistema
def menuPrincipal():
    print("Seleccione una opcion:")              # Imprime opciones del menú
    print(" 1. Generar Rutas")
    print(" 2. Graficar rutas")
    print(" 3. Ver tablero")
    print(" 4. Modo automatico (todo en uno)")
    print(" 5. Salir")
    while True: 
        n = int(input())                         # Solicita al usuario una opción
        if n >= 1 and n <= 5:                    # Valida opción
            if(n==1):                            # Ir al menú de generación de rutas
                menuGenerar()
            elif(n==2):                          # Ir al menú de graficación
                menuGrafo()
            elif(n==3):                          # Ir al menú del tablero animado
                menuTablero() 
            elif(n==4):                          # Ejecuta modo automático completo
                automatico() 
            elif(n==5):                          # Sale del programa
                exit()
            break
        else:
            print('Selecciona una opción válida:')
def menuGenerar():
    print("Seleccione una opcion:")
    print(" 1. Dar cadena")                      # El usuario ingresa las cadenas manualmente
    print(" 2. Generar cadena aleatoria")        # Se generan automáticamente
    j = int(input())                             # Opción del usuario

    if(j==1):
        cadena1= input("Ingrese cadena para pieza 1:")   # Cadena manual para pieza 1
        cadena2= input("Ingrese cadena para pieza 2:")   # Cadena manual para pieza 2
        Generar_Rutas(cadena1, cadena2)                  # Genera rutas en base a esas cadenas
    elif (j==2):
        longitud = int(input("De cuanta longitud?:"))    # Pide longitud de las cadenas
        iguales= input("Ambas cadenas son iguales?? s/n:")  # Determina si deben ser idénticas
        
        cadena1=""
        for i in range(longitud-1):                      # Genera la cadena aleatoria, menos el último caracter
            nr1= np.random.randint(0,2)
            if nr1 ==0:
                cadena1 += 'w'
            else:
                cadena1 += 'b'
        cadena1+='w'                                     # Asegura que termine en 'w'

        if(iguales=='n'):                                # Si son distintas, genera segunda cadena
            cadena2=""
            for i in range(longitud-1):
                nr2= np.random.randint(0,2)
                if nr2 ==0:
                    cadena2 += 'w'
                else:
                    cadena2 += 'b'
            cadena2+='w'    
            
            Generar_Rutas(cadena1, cadena2)              # Genera rutas con ambas
            print(f"Cadena1:{cadena1}")
            print(f"Cadena2:{cadena2}")
        else: 
            Generar_Rutas(cadena1, cadena1)              # Usa la misma cadena para ambas
            print(f"Cadena:{cadena1}")
    
    menuPrincipal()                                      # Regresa al menú principal

def menuGrafo():
    print("Cual ruta quiere graficar:")
    print(" 1. Ganadoras 1")
    print(" 2. Ganadoras 2")
    print(" 3. Todas las posibles de 1")
    print(" 4. Todas las posibles de 2")
    n = int(input())                                     # Opción del usuario
    if(n==1):
        graficarRutas("rutas/rutas_1.csv")
    elif(n==2):
        graficarRutas("rutas/rutas_2.csv")
    elif(n==3):
        graficarRutas("rutas/rutas_posibles_1.csv")
    elif(n==4):
        graficarRutas("rutas/rutas_posibles_2.csv")
    
    menuPrincipal()                                      # Regresa al menú principal

def menuTablero():
    n = int(input("Con que pieza quiere que inicie?: ")) # Pregunta cuál pieza inicia
    if(n==1):  
        pieza=1
    elif n==2: 
        pieza=2

    Tablero("rutas/rutas_1.csv","rutas/rutas_2.csv",n)   # Muestra la animación del tablero
    menuPrincipal()

def automatico():
    longitud = 10  # o el valor que desees

    # Genera cadena para pieza 1 (termina en 'w')
    cadena1 = ""
    for i in range(longitud - 1):
        nr1 = np.random.randint(0, 2)
        if nr1 == 0:
            cadena1 += 'w'
        else:
            cadena1 += 'b'
    cadena1 += 'w'

    # Genera cadena para pieza 2 (termina en 'b')
    cadena2 = ""
    for i in range(longitud - 1):
        nr2 = np.random.randint(0, 2)
        if nr2 == 0:
            cadena2 += 'w'
        else:
            cadena2 += 'b'
    cadena2 += 'b'

    Generar_Rutas(cadena1, cadena2)                      # Genera rutas
    print(f"Cadena1: {cadena1}")
    print(f"Cadena2: {cadena2}")

    graficarRutas("rutas/rutas_1.csv")                   # Muestra grafo de rutas ganadoras de 1
    graficarRutas("rutas/rutas_2.csv")                   # ... de pieza 2
    graficarRutas("rutas/rutas_posibles_1.csv")          # ... todas las posibles de 1
    graficarRutas("rutas/rutas_posibles_2.csv")          # ... todas las posibles de 2

    Tablero("rutas/rutas_1.csv", "rutas/rutas_2.csv", 1) # Anima la simulación con pieza 1 comenzando

    menuPrincipal()                                      # Regresa al menú principal

# Se ejecuta el menú principal cuando se corre el script
menuPrincipal()
