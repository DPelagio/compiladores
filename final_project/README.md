# Proyecto final Diseño de Compiladores

El objetivo del proyecto es generar a través de reglas gramaticales un intérprete, en nuestro caso, de un lenguaje definido por nosotros y ser ejecutado por cualquier equipo de cómputo.

Nuestro lenguaje llamado Polite Language, es capaz de interpretar sentencias de control como: while; de condición: if, if-else, así como asignación de valores a variables y ejecución de funciones, similar a como se haría en otros de lenguaje de programación.

## Desarrollo

Nuestro proyecto fue desarrollado usando ANTLR (ANother Tool for Language Recognition), usando como base el lenguaje de programación Python para usar el Lexer y Parser que nos proporciona ANTLR para posteriormente manipular el árbol de sintaxis.

## Instalación

Para correr el proyecto se debe tener instalado las siguientes herramientas:
- Java, versión 1.8
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

## Run

Para ejecutar el proyecto puede utilizar el archivo de test del proyecto, es necesario pasarle como referencia el path del archivo que desee analizar

```
python3 main.py simple_test
```

donde `simple_test` es el nombre del archivo

## Referencias

Para crear este proyecto nos basamos en varios tutoriales y demos que encontramos acerca de cómo utilizar la herramienta ANTLR, al igual de cómo generar la gramática válidad para la herramienta, a continuación los links de donde tomamos tutoriales como referencias:

1. https://medium.com/@fwouts/a-quick-intro-to-antlr4-5f4f35719823
2. http://andrej-mohar.com/blog/antlr-the-basics-of-parsing-programming-languages-source-code
3. https://medium.com/@raguiar2/building-a-working-calculator-in-python-with-antlr-d879e2ea9058
4. https://hackernoon.com/creating-a-scripting-language-with-antlr-part-1-1b42c3e4d718
5. https://github.com/antlr/grammars-v4



