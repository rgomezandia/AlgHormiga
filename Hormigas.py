#!/usr/bin/python
# -*- coding: utf-8 -*-
# Programa Cliente

import sys
import random
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix

def numRandomicoReal():
    return random.random()
def numRandomicoUnoToN(N):
    return random.randint(1, N)

def generarUnaHormiga(tamano):
    tmp = list(range(tamano))
    random.shuffle(tmp)
    return(tmp)

def initColonia(tamColonia,archEntrada):
    poblacion = []
    puntosDeinicioHormigas = list(range(len(archEntrada)))
    random.shuffle(puntosDeinicioHormigas)
    for i in range(tamColonia):
        if(len(puntosDeinicioHormigas)==0): #CONDICION EN CASO DE QUE EL TAMAÑO DE LA COLONIA SEA MAYOR A LOS PUNTOS DE INICIO (ASI PODRAN REPETIRSE ALGUNAS)
            puntosDeinicioHormigas = list(range(len(archEntrada)))
            random.shuffle(puntosDeinicioHormigas)
        nuevaHormiga = [puntosDeinicioHormigas.pop()]
        poblacion.append(nuevaHormiga)
    return poblacion

def initFeromona(costoHormigaInicial, tam):
    mFerom = np.ones((tam, tam))
    mFerom = mFerom/costoHormigaInicial
    np.fill_diagonal(mFerom, 0)
    return mFerom

def selectNwSegmentoRuta(laHormiga, T, n, q0, B):

    numeroRandomico = numRandomicoReal()
    N=[]
    temp = generarUnaHormiga(52)
    for item in temp:
        if item not in laHormiga:
            N.append(item)

    if(numeroRandomico<=q0): #Si se cumple, entonces EQ 1 con probabilidad q0 #numRandomicoReal()<=q0
        mejorRuta = 0
        valorRuta = 0
        for i in N:
            tmp = T[laHormiga[len(laHormiga)-1]][i] * (n[laHormiga[len(laHormiga)-1]][i] ** B) #ECUACION 1
            if(valorRuta < tmp):
                valorRuta = tmp
                mejorRuta = i
        laHormiga.append(mejorRuta)
    else: #Sino la ecuacion 2!
        valores = []
        valores2 = []
        rutas = []
        sumador = 0
        for i in N:
            valores.append(T[laHormiga[len(laHormiga)-1]][i] * (n[laHormiga[len(laHormiga)-1]][i] ** B))
            rutas.append(i)
        sumador = sum(valores)
        valDivididos = list(map(lambda x: x / sumador, valores))
        for i in range(len(valDivididos)):
            if i == 0:
                valores2.append(valDivididos[i])
            else:
                valores2.append(valDivididos[i]+valores2[i-1])
        laHormiga.append(rutas[selecIndividuoRuleta(valores2)])
    return(laHormiga)


def selecIndividuoRuleta(valores):
    seleccionAleatorio = numRandomicoReal()
    for x in range(len(valores)):
        if (x == 0):
            if (seleccionAleatorio < valores[x]):
                seleccion = x
        else:
            if seleccionAleatorio > valores[x - 1] and seleccionAleatorio < valores[x]:
                seleccion = x
    return seleccion  # devuelvo el individuo seleccionado

def actLocalFerom(T,alfa,i,j,T0):
    T[i][j] = ((1 - alfa) * T[i][j]) + (alfa * T0)  #ECUACION 4
    return T

def actGlobalFerom(T,alfa, delta, hormigona):
    #Su limpieza de foromonas
    T = np.multiply(T, (1 - alfa))
    #Ahora aplicamos la ecuacion 3
    for i in range(len(hormigona)-1):
            T[i][i+1] = (1-alfa)*T[i][i+1] + alfa * delta #ECUCACION 3
    return T

def evaluarRutadeHormiga(hormiga, Mdist):
    coste = 0.0
    for i in range (len(hormiga)):
        if(i==len(hormiga)-1):
            coste = coste + Mdist[hormiga[i]][hormiga[0]]
        else:
            coste = coste + Mdist[hormiga[i]][hormiga[i+1]]
    return coste

def seleccionMejorSolucion(poblacionTotal,Mdist):
    newValor = 0
    posicion = 0
    for j in range(len(poblacionTotal)):
        valorInicial = evaluarRutadeHormiga(poblacionTotal[j],Mdist)
        if (valorInicial > newValor):
           posicion = j
           newValor = valorInicial
    return (poblacionTotal[posicion])


def lecturaArchivo(path):
    data = []
    with open(path) as f:
        for line in f.readlines()[6:-1]:
            _, *b = line.split()
            data.append((float(i) for i in b))
    coordenadas = pd.DataFrame(data, columns=['x_coord', 'y_coord'])
    matrizDistancias = pd.DataFrame(distance_matrix(coordenadas.values, coordenadas.values))
    del (matrizDistancias[52])
    matrizDistancias = matrizDistancias.drop([52])
    return matrizDistancias

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("No ha ingresado todos los parametros solicitados.")
        sys.exit(0)

    archEntrada = lecturaArchivo(sys.argv[1]) #Matriz Distancias
    MatrizHeuristica = np.where(archEntrada != 0, 1/archEntrada, 0) #Matriz Heuristica
    semilla = int(sys.argv[2])
    tamColonia = int(sys.argv[3])
    numIteraciones = int(sys.argv[4])
    evaporacionAlfa = float(sys.argv[5])
    pesoBeta = float(sys.argv[6])
    limiteProbQ0 = float(sys.argv[7])

    random.seed(semilla)  # Asignamos la semilla al random.
    hormigaInicial = generarUnaHormiga(len(archEntrada))
    costeHormigaInicial = evaluarRutadeHormiga(hormigaInicial,archEntrada)
    mFerom = initFeromona(costeHormigaInicial,len(archEntrada))
    mejorSolucion = costeHormigaInicial
    mejorSolucionHormiga = hormigaInicial

    for i in range (numIteraciones):
        #ASIGNAMOS UNA HORMIGA POR VERTICE EN EL GRAFO
        poblacionInicial = initColonia(tamColonia, MatrizHeuristica)
        #("Poblacion inicial: ",poblacionInicial, " de la iteracion: ", i)

        for z in range(51):
            for p in range (tamColonia):
                poblacionInicial[p] = selectNwSegmentoRuta(poblacionInicial[p], MatrizHeuristica,mFerom,limiteProbQ0,pesoBeta)
                temporal = poblacionInicial[p]
                mFerom = actLocalFerom(mFerom, evaporacionAlfa, temporal[len(temporal)-2],temporal[len(temporal)-1],1/costeHormigaInicial)

        #print("Poblacion total hormigas: ", poblacionInicial, " de la iteracion: ", i)

        hormigaGlobalBest = seleccionMejorSolucion(poblacionInicial,archEntrada) #seleccionamos la mejor hormiga de la poblacion
        costeHormigaGlobalBest = evaluarRutadeHormiga(hormigaGlobalBest, archEntrada) #obtenemos su coste
        if (mejorSolucion>costeHormigaGlobalBest): #la comparamos para reemplazarla o no
            mejorSolucion = evaluarRutadeHormiga(hormigaGlobalBest,archEntrada)
            mejorSolucionHormiga = hormigaGlobalBest;
        mFerom = actGlobalFerom(mFerom, evaporacionAlfa, 1/costeHormigaGlobalBest, hormigaGlobalBest) #Terminamos actualizando segun la mejor solucion actual.

    print("la mejor solucion encontrada es :", mejorSolucionHormiga, "de coste: ", mejorSolucion)
