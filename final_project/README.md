# Polite Language 
## Proyecto Final Diseño de Compiladores

## Descripción

El objetivo del proyecto es generar a través de un conjunto de reglas gramaticales un intérprete, en nuestro caso, de un lenguaje definido por nosotros y ser ejecutado en cualquier equipo de cómputo.

Nuestro lenguaje llamado Polite Language, acepta la sintaxis básica de otros lenguajes de programación y es capaz de interpretar sentencias de control como: `while`; de condición: `if`, `if-else`, así como asignación de valores a variables de tipo: `int`, `float`, `string`, `char` y `bool`; creación de funciones y ejecución de las mismas creadas por nosotros además de funciones externas propias de Python como `print()`, se adicionaron características a nuestro lenguaje que hacen única la forma de escribir código a lo convencional.

## Desarrollo

Nuestro proyecto fue desarrollado usando ANTLR (ANother Tool for Language Recognition), en conjunto con el lenguaje de programación Python.

ANTLR es una herramienta poderosa que nos genera parsers para leer, procesar, ejecutar o traducir texto estructurado. Se utiliza en frameworks, librerías y sobre todo en lenguajes nuevos.

La manera en la que utilizamos ANTLR fue la siguiente:
- Generamos un archivo con extensión `.g4` donde describimos la gramática de nuestro lenguaje
- Ejecutamos el comando `antlr4 -Dlanguage=Python3 PL.g4`
- Esto nos genera un conjunto de archivos Python que contienen el Lexer, Parser y un Árbol sintáctico para parsear nuestros archivos de programa
- A partir de estos archivos generados internamente podemos utilizarlos para darle la lógica de ejecución

ANTLR nos permite crear también una herramienta llamada visitor, la cual nos permite manejar el archivo sobre el árbol sintáctico y hacer type conversion, además de error handling.

## Instalación

Para correr el proyecto y los comandos anteriores se debe tener instalado las siguientes herramientas:
- Java, versión 1.8
- Antlr
- Python, versión 3.7
- Dependencia de Antlr para Python

Los siguientes pasos son aplicables para Sistemas Operativos Linux y MacOS

### Instalación de Java
Se recomienda utilizar la última versión de Java Development Kit

1. Descargar el paquete en dependencia del tipo de Sistema Operativo y arquitectura del equipo de cómputo [Descargar JDK](https://www.oracle.com/mx/java/technologies/javase/javase-jdk8-downloads.html)

2. Copiar el paquete al directorio `/opt/` que es el directorio adecuado para el software de terceros, en este caso Java

3. Descompactar el paquete JDK descargado
    ```
    tar xzf jdk-8u251-linux-x64.tar.gz
    ```

4. Instalar con el comando alternatives
    ```
    cd jdk1.8.0_251/
    alternatives --install /usr/bin/java java /opt/jdk1.8.0_251/bin/java 2
    alternatives --config java
    ```

5. Configuración de comandos `javac` y `jar`
    ```
    alternatives --install /usr/bin/jar jar /opt/jdk1.8.0_251/bin/jar 2
    alternatives --install /usr/bin/javac javac /opt/jdk1.8.0_251/bin/javac 2
    alternatives --set jar /opt/jdk1.8.0_251/bin/jar
    alternatives --set javac /opt/jdk1.8.0_251/bin/javac
    ```

6. Validar versión de Java instalado
    ```
    java -version
    ```
    ```
    java version "1.8.0_251"
    Java(TM) SE Runtime Environment (build 1.8.0_251-b08)
    Java HotSpot(TM) 64-Bit Server VM (build 25.251-b08, mixed mode)
    ```

7. Configuración de variables de ambiente, dichas variables deben ser guardadas en el archivo `.bashrc` para que se mantengan visibles las referencias para cualquier programa, en nuestro caso ANTLR pueda ejecutar sus comandos propios
    ```
    export JAVA_HOME=/opt/jdk1.8.0_251
    export JRE_HOME=/opt/jdk1.8.0_251/jre
    export PATH=$PATH:/opt/jdk1.8.0_251/bin:/opt/jdk1.8.0_251/jre/bin
    ```

### Instalación de Python
Se recomienda usar la versión 3.7 de Python para correr el proyecto

* MacOS
  - Instalar con brew `brew install python3`
* Linux
  - Instalar con el instalador de paquetes del Sistema Operativo `sudo apt-get install python3.7` para distribuciones Debian o `sudo dnf install python3` para distribuciones Red Hat

### Instalación de ANTLR
Para generar el Lexer y Parser de cualquier gramática se debe instalar ANTLR

1. Descargar ANTLR en el directorio `/usr/local/lib`
    ```
    cd /usr/local/lib
    sudo curl -O https://www.antlr.org/download/antlr-4.8-complete.jar
    ```
2. Guardar variables de ambiente y alias de comandos en `.bashrc`, de esta manera con sólo ejecutar los comandos `antlr4` o `grun` se ejecutaran las herramientas de ANTLR
    ```
    export CLASSPATH="/usr/local/lib/antlr-4.8-complete.jar:$CLASSPATH"
    alias antlr4='java -jar /usr/local/lib/antlr-4.8-complete.jar'
    alias grun='java org.antlr.v4.gui.TestRig'
    ```


### Instalación de ANTLR para Python
ANTLR tiene la capacidad de generar los archivos para una lista de lenguajes de programación como: Java, JavaScript, Python, C#. En nuestro caso utilizaremos Python y para eso ejecutaremos el siguiente comando para instalar la dependencia
    
    ```
    pip install antlr4-python3-runtime
    ```

Una vez que tenemos las herramientas instaladas podremos ejecutar el proyecto sin problema alguno, de igual manera es necesario para realizar cualquier cambio ya sea en las reglas gramaticales o en la forma en que es analizado.


## Ejecución

Para ejecutar el proyecto puede utilizar el archivo de test del proyecto, es necesario pasarle como referencia el path del archivo que desee analizar

```
python3 main.py programs/test.please
```

donde `test.please` es el nombre del archivo


## Sintaxis

La sintaxis de Polite Language se diseñó para que fuese sencillo escribir líneas de código. Cabe destacar que es case sensitive por lo que es importante pedirle las cosas de manera clara a nuestro lenguage.

Todo programa debe iniciar con la siguiente frase `Dear Program,` y terminar con `Thank you.` Como cuerpo del programa se pueden incluir las sentencias de control, condición, variables y funciones que se necesiten.


### Sentencias de condición IF, IF ELSE
Para escribir una sentencia `IF` se debe seguir la siguiente sintaxis

> if -> CONDICIÓN : { OPERACIÓN please }

donde:
  * `if` es una palabra reservada como en los demás lenguajes de programación
  * `->` son los caracteres para indicar que iniciará una nueva expresión, en este caso una expresión de condición
  * `CONDICIÓN` es la expresión que evaluará un conjunto de operaciones que devuelve True en el caso de que se cumpla la condición y entrará al cuerpo del IF, False caso contrario
  * `:` caracter para indicar el cierre de la expresión de condición
  * `{` caracter para indicar el inicio del cuerpo del IF
  * `OPERACIÓN` es una expresión que debe describir qué operación realizar
  * `please` es el fin de la sentencia de operación y con la cual podrá ejecutarse, si no se escribe `please` el programa no funcionará ya que no está recibiendo la petición de manera atenta
  * `}` cierre del cuerpo del IF

En el caso de necesitar `ELSE` se debe anexar lo siguiente a la sintaxis anterior

> else { OPERACIÓN please }

donde:
  * `else` es la palabra reservada
  * `{` inicio del cuerpo del else
  * `OPERACIÓN` son las expresiones que describen las operaciones que se deben ejecutar
  * `please` cada sentencia de operación debe terminar con `please`
  * `}` cierre del cuerpo del else


### Sentencia de control WHILE
Para escribir un ciclo con `WHILE` se debe seguir la siguiente sintaxis

> while -> CONDICIÓN : { OPERACIÓN please }

donde:
  * `while` es la palabra reservada para iniciar el ciclo
  * `->` indica el inicio de una sentencia, en este caso la evaluación de una condición
  * `CONDICIÓN` conjunto de operaciones que deben devolver True o False en función de las comparaciones que se realicen
  * `:` fin de sentencia de comparación
  * `{` inicio del cuerpo de while
  * `OPERACIÓN` expresión que representa la ejecución de una operación, alguna sentencia de condición, llamada a una función u otro ciclo
  * `please` en el caso de ejecutar una sentencia se debe anexar esta palabra para poder ejecutarse
  * `}` fin del cuerpo de while


### Declaración de FUNCIONES
Para escribir una función se debe declarar de la siguiente forma

> const NAME_FNCTN = (ARGS) => {OPERACIÓN please}
> const NAME_FNCTN = { OPERACIÓN please }

El primer caso es cuando se requiere pasarle un conjunto de parámetros, el segundo funciona perfecto cuando no se tiene que pasar parámetros.

donde:
  * `¢onst` es la palabra reservada para indicar el nombre de una función
  * `NAME_FNCTN` es el nombre que tendrá la función, el cual permite caracteres alfanuméricos, guiones medios y bajos
  * `=` caracter para asignar la referencia de la función declarada
  * `(` caracter para iniciar la declaración de parámetros
  * `ARGS` conjunto de parámetros que se pasarán al cuerpo de la función a evaluar
  * `)` caracter de cierre de declaración de parámetros
  * `=>` caracteres para indicar que terminar la declaración de variables e inicia el cuerpo de la función y el valor que retornará
  * `{` caracter de inicio del cuerpo de la función
  * `OPERACIÓN` conjunto de expresiones que se ejecutarán dentro de la función, permite la llamada recursiva a si misma como función, a otras funciones u otro tipo de sentencia de control o condición
  * `please` palabra reservada para ejecutar una operación
  * `}` cierre del cuerpo de la función

Para llamar funciones se debe declarar de esta forma

> call NAME_FNCTN(ARGS) please

donde:
  * `call` es una palabra reservada para llamar a la función
  * `NAME_FNCTN` nombre de la función previamente declarada
  * `(ARGS)` conjunto de parámetros que se pasaran a la función a evaluar
  * `please` palabra reservada para ejecutar la función


## Asignación de variables
Para asignar valores mediante el uso de variables se requiere la siguiente sintaxis

> save VALUE in @NAME_VAR please

donde:
  * `save` es la palabra reservada para indicar que se debe asignar el valor a la variable
  * `VALUE` valor a guardar de tipo: int, float, string, char o bool
  * `in` palabra para indicar en donde se debe guardar
  * `@NAME_VAR` nombre de la variable alfanumérica, debe iniciar con `@` para poder definir la variable correctamente
  * `please` palabra reservada para ejecutar la sentencia

## Ejecución de PRINT
Si se requiere ejecutar imprimir en consola se puede usar la siguiente sintaxis

> say -> @NAME_VAR please

donde:
  * `say` palabra reservada para la función `print`
  * `->` caracteres para indicar que expresión debe ser impresa
  * `@NAME_VAR` nombre de la variable a imprimir, o bien operación matemática que se evaluará y devolverá el resultado
  * `please` palabra reservada para ejecutar la sentencia


## Escribir código con Polite Language
Con base en la sintaxis descrita se puede escribir el algoritmo que se requiera con extensión `.please` y ejecutarse con `python3 main.py nuevo_programa.please`