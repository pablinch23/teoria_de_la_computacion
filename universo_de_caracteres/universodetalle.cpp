#include <iostream>     // Librería para entrada/salida estándar (como cout y cin)
#include <bitset>       // Librería para manipular datos binarios (representación de bits)
#include <fstream>      // Librería para manejar archivos (lectura y escritura)
#include <string>       // Librería para trabajar con cadenas de texto (std::string)
#include <cstdlib>      // Librería para funciones como rand() y srand()
#include <ctime>        // Librería para obtener el tiempo actual (para semilla de aleatoriedad)
using namespace std;    // Evita tener que usar std:: antes de cin, cout, string, etc.

// Esta función genera y escribe todas las combinaciones binarias de una longitud dada
// Parámetros:
// - length: longitud de las combinaciones (por ejemplo 3 -> genera 000, 001, ..., 111)
// - file: archivo de salida para escribir las combinaciones
// - first: bandera para saber si se está escribiendo la primera combinación (para no poner coma antes)
void generate_combinations_for_length(int length, ofstream &file, bool &first) {

    // Caso especial: si la longitud es 0, se escribe solo "0"
    if (length == 0) {
        if (!first) file << ", "; // Si no es la primera, agrega coma antes
        file << "0";              // Escribe "0"
        first = false;            // Marca que ya se escribió algo
        return;                   // Termina la función
    }
    
    // Crea un objeto bitset de 1000 bits (todos inicializados en 0)
    std::bitset<1000> Bits;

    // Convierte el bitset a cadena de texto, luego toma los últimos "length" bits
    string comb = Bits.to_string().substr(1000 - length);

    // Si ya se escribió algo antes, se pone una coma
    if (!first) file << ", ";

    // Escribe la combinación actual al archivo
    file << comb;

    // Marca que ya se escribió algo
    first = false;

    // Bucle para generar todas las combinaciones hasta que sean todos 1's (ej: 111)
    while (true) {
        bool allOnes = true; // Supone que ya están todos en 1

        // Verifica si todos los bits de la combinación actual son 1
        for (int i = 0; i < length; i++) {
            if (!Bits[i]) {       // Si algún bit es 0...
                allOnes = false;  // ...no hemos llegado al final
                break;            // Sale del for
            }
        }

        // Si ya están todos los bits en 1, termina el ciclo
        if (allOnes)
            break;

        // Simula una suma binaria para incrementar en 1 la combinación binaria actual
        bool carry = true; // Lleva inicial en 1 (como si estuviéramos sumando 1)
        for (int i = 0; i < length; i++) {
            bool bit = Bits[i];             // Valor actual del bit
            Bits[i] = bit ^ carry;          // XOR: suma binaria del bit con el carry
            carry = bit && carry;           // Nuevo carry: si ambos eran 1
            if (!carry)                     // Si no hay acarreo, terminamos la suma
                break;
        }

        // Convierte el nuevo bitset a string y toma los últimos "length" bits
        comb = Bits.to_string().substr(1000 - length);

        // Escribe al archivo con coma antes
        file << ", " << comb;
    }
}

// Función principal del programa
int main(){
    int n;         // Variable para almacenar la longitud máxima (universo)
    char mode;     // Modo de ejecución: 'a' automático o 'm' manual
    
    // Solicita al usuario elegir el modo
    cout << "¿Modo automático (a) o manual (m)? ";
    cin >> mode;

    // Si el usuario elige modo automático
    if (mode == 'a' || mode == 'A') {
        srand(time(0));               // Inicializa el generador de números aleatorios con la hora actual
        n = rand() % 1001;            // Genera un número aleatorio entre 0 y 1000
        cout << "Modo automático. Valor de n: " << n << endl;
    } 
    // Si el usuario elige modo manual
    else if (mode == 'm' || mode == 'M') {
        cout << "Ingrese un valor entero para el universo (max longitud): ";
        cin >> n;                     // Lee el valor ingresado
    } 
    // Si el modo no es válido
    else {
        cout << "Modo no reconocido. Saliendo." << endl;
        return 1;                     // Termina el programa con error
    }

    // Validación del rango del valor n
    if (n < 0 || n > 1000) {
        cout << "El valor de n debe estar entre 0 y 1000." << endl;
        return 1; // Termina el programa con error
    }

    // Intenta abrir el archivo para escribir combinaciones
    ofstream file("binaries1.txt");   // Abre archivo llamado "binaries1.txt" para escritura
    if (!file) {
        cerr << "Error al abrir el archivo." << endl;
        return 1; // Si no se pudo abrir, termina el programa con error
    }

    // Escribe la apertura de un conjunto en el archivo (como un arreglo en texto)
    file << "{";
    bool first = true; // Variable para saber si se está escribiendo la primera combinación

    // Escribe la combinación de longitud 0 (es decir, "0")
    generate_combinations_for_length(0, file, first);

    // Llama a la función para cada longitud desde 1 hasta n (inclusive)
    for (int i = 1; i <= n; i++){
        generate_combinations_for_length(i, file, first);
    }

    // Cierra el conjunto en el archivo (corchete de cierre)
    file << "}";

    // Cierra el archivo
    file.close();

    // Informa al usuario que se ha generado el archivo
    cout << "Archivo 'binaries.txt' generado." << endl;
    
    return 0; // Fin exitoso del programa
}
