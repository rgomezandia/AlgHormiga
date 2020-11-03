#!/usr/bin/python
# -*- coding: utf-8 -*-
# Programa Cliente

import sys
import random


def numRandomicoReal():
    return random.random()
def numRandomicoUnoToN(N):
    return random.randint(1, N)

def initColonia(tamPoblacion, tamTablero):
    poblacion = []
    for i in range(tamPoblacion):
        tmp = list(range(1, tamTablero + 1))
        random.shuffle(tmp)
        poblacion.append(tmp)
    return poblacion

def initFeromona(tamPoblacion, tamTablero):
    poblacion = []
    for i in range(tamPoblacion):
        tmp = list(range(1, tamTablero + 1))
        random.shuffle(tmp)
        poblacion.append(tmp)
    return poblacion

def selectNwSegmentoRuta():
    return 0

def actLocalFerom():
    return 0

def actGlobalFerom():
    return 0

def evaluarRutadeHormiga():
    return 0


def selecIndividuoRuleta(poblacion):
    fitnes = []  # o ruleta...
    sumador = 0.
    temp = 0  # dice que no se usa, pero bajo mi logica deberia estar aqui.

    for number in range(
            len(poblacion)):  # este for es solo para obtener la sumatoria completa de la version invertida. 1/x
        if (calcFitness(poblacion[
                            number]) == 0):  # CLARO ESTA, QUE SI EL FITNESS ES 0 ENTONCES NO PODEMOS DIVIDIR 1/0 , POR ENDE LO VOLVEREMOS 1, PARA CONSIDERARLO UN VALOR CON MAYOR PROBABILIDAD, YA QUE ES PERFECTO.
            sumador = (1 / 1) + sumador
        else:
            sumador = (1 / calcFitness(poblacion[number])) + sumador

    for x in range(len(poblacion)):
        if x == 0:
            if (calcFitness(poblacion[x]) == 0):
                fitnes.append((1 / 1) / sumador)
            else:
                fitnes.append((1 / calcFitness(poblacion[x]) / sumador))
        else:
            if (calcFitness(poblacion[x]) == 0):
                temp = (1 / 1) / sumador
            else:
                temp = (1 / calcFitness(poblacion[x])) / sumador
            fitnes.append((temp) + fitnes[x - 1])

    seleccion = numRandomicoReal()
    for x in range(len(fitnes)):
        if (x == 0):
            if (seleccion < fitnes[x]):
                seleccion = x
        else:
            if seleccion > fitnes[x - 1] and seleccion < fitnes[x]:
                seleccion = x
    return poblacion[seleccion]  # devuelvo el individuo seleccionado

def seleccionHormigaGlobal(poblacionTotal):
    for j in range(len(poblacionTotal)):
        valorInicial = calcFitness(poblacionTotal[j])
        posicion = j
        for i in range(j, len(poblacionTotal)):
            newValor = calcFitness(poblacionTotal[i])
            if (valorInicial > newValor):
                posicion = i
                valorInicial = newValor
        poblacionTotal.insert(j, poblacionTotal.pop(posicion))
    return (poblacionTotal[0:int(len(poblacionTotal) / 2)])


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("No ha ingresado todos los parametros solicitados.")
        sys.exit(0)

    archEntrada = String(sys.argv[2])
    semilla = int(sys.argv[2])
    tamColonia = int(sys.argv[3])
    numIteraciones = int(sys.argv[4])
    evaporacionAlfa = int(sys.argv[5])
    pesoBeta = int(sys.argv[6])
    limiteProbQ0 = int(sys.argv[7])  # generaciones

    random.seed(semilla)  # Asignamos la semilla al random.



