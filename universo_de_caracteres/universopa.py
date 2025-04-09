import matplotlib.pyplot as plt
import numpy as np

def read_combinations_from_file(filename):
    """
    Lee el archivo generado por el código en C y extrae las combinaciones binarias.
    Se espera que el contenido esté en una sola línea, con formato:
    {comb1, comb2, comb3, ...}
    """
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Eliminar las llaves de apertura y cierre si están presentes
    if content.startswith("{") and content.endswith("}"):
        content = content[1:-1]
    # Dividir por comas y eliminar espacios en blanco
    combos = [item.strip() for item in content.split(",") if item.strip()]
    return combos

def generate_plots(combos):
    # Índices para el eje X
    indices = list(range(len(combos)))
    
    # Contar ceros y unos en cada combinación
    zeros = [comb.count('0') for comb in combos]
    ones  = [comb.count('1') for comb in combos]
    
    # Convertir cada combinación en un entero (base 2)
    values = [int(comb, 2) for comb in combos]
    
    # Gráfico 1: Conteo de ceros y unos
    plt.figure()
    plt.scatter(indices, zeros, s=10, label='Ceros', color='blue')
    plt.scatter(indices, ones, s=10, label='Unos', color='red')
    plt.xlabel('Índice de Combinaciones')
    plt.ylabel('Conteo de Ceros / Unos')
    plt.title('Conteo de Ceros y Unos en Combinaciones Binarias')
    plt.legend()
    plt.show()
    
    # Gráfico 2: Valor entero en escala logarítmica
    values_log = [np.log10(v + 1) for v in values]  # Se suma 1 para evitar log(0)
    plt.figure()
    plt.scatter(indices, values_log, s=10, label='Valor (log10)', color='green')
    plt.xlabel('Índice de Combinaciones')
    plt.ylabel('Log10(Valor + 1)')
    plt.title('Gráfico Logarítmico de las Combinaciones')
    plt.legend()
    plt.show()

def main():
    filename = 'binaries.txt'
    combos = read_combinations_from_file(filename)
    print(f"Se han leído {len(combos)} combinaciones desde '{filename}'.")
    generate_plots(combos)

if __name__ == '__main__':
    main()
