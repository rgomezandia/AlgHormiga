# Algoritmo Colonia de hormigas



### Acerca de este Trabajo

Esta es una implementación en Python del algoritmo de colonia de hormigas.

### Parametros del Cliente   

1. __archivoDeEntrada__ : nombre del archivo con su extension (berlin52.tsp)
1. __semilla__ : numero entero que sirve para generar los numeros aleatorios dentro de python.
2. __tamColonia__: numero entero que indica el tamaño de la colonia o numero de hormigas.
3. __numIteraciones__ : numero entero que representa el numero de iteraciones como condicion de termino.
4. __evaporacionAlfa__: numero real que representa el factor de evaporacion de la feromona (α).
5. __pesoBeta__ : numero real que representa el peso del valor de la heuristica (β).
6. __limiteProbQ0__: numero real que representa la probabilidad limite (q0).


### Instrucciones para correr el programa en una terminal linux

~~~
$ git clone https://github.com/rgomezandia/AlgHormiga.
~~~


### Ejecutar Programa
~~~
 $ python3 Hormigas.py "__archivoDeEntrada__" "__semilla__" "__tamColonia__" "__numIteraciones__" "__evaporacionAlfa__" "__pesoBeta__" "__limiteProbQ0__"
~~~
