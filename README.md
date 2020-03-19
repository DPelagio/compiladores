# compiladores
Manual de Usuario
Pre-requisitos:
   1. Tener instalado python3 y pip3
   2. Instalar las dependencias con el comando: pip3 install -r requirements.txt

Intrucciones de Uso:
   1. Correr el programa con el comando: python3 tarea1.py
   2. Introducir el nombre del archivo donde se encuentra el alfabeto y la expresion regular, con el siguiente formato:
      - Alfabeto: Separado por espacios, cada caracter que conforma todo el alfabeto. En la primera linea
      - Expresion Regular: En la siguiente linea, la expresion regular, todo sin espacios y los caracteres reservados son: . | * + ( ) ?
      Ejemplo: 
         0 1
         01*
   3. Introducir el numero de la opcion a elegir:
      I. Obtener el NFA de la expresion regular dada. (el json y el grafo dibujado)
      II. Obtener el DFA de la expresion regular dada. (el json y el grafo dibujado)
      III. Probar una cadena con el lenguaje de la expresion regular.
      IV. Salir