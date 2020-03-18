#Alejandra Tubilla      A01022960
#Joan Andoni González   A00569929
#German Torres          A01651423

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

estados = [0]
estadoFinal = 0
estadoActual = 0
automata = []
alfabeto = []
caracteresEspeciales = ['(', ')', '|']

#Funcion para crear el NFA a partir de la expresion regular
def NFA(expresionRegular, star, fin): 

    global estadoFinal
    global estadoActual
    padre = False
    contador = 0
    expresionRegularParte = ''
    estadoAnterior = estadoFinal


    if star == True:

        state = [estadoFinal, 'ep', estadoFinal+1+estadoActual]
        estadoFinal += (1 + estadoActual)
        if estadoActual != 0: estadoActual = 0

        if state not in automata:
            automata.append(state)

    #Dividir la expresion regular por partes
    for index, caracter in enumerate(expresionRegular):

        if caracter not in alfabeto and caracter not in caracteresEspeciales:
            alfabeto.append(caracter)
        #Dentro del parentesis
        if caracter == '(':
            padre = True            
            if contador > 0:
                expresionRegularParte+= caracter

            contador += 1

        elif caracter == ')':

            contador -= 1

            if contador > 0:
                expresionRegularParte+= caracter

            elif contador == 0:
                if index < len(expresionRegular) -1 and expresionRegular[index +1] == '*':

                    NFA(expresionRegularParte, True, 0)


                else: 
                    NFA(expresionRegularParte, False, 0)

                expresionRegularParte = ''

        elif contador > 0:
                expresionRegularParte+= caracter
    #con OR
    if padre == False:
        if '|' in expresionRegular:
            estadoOR = expresionRegular.split('|')
            estadosF = expresionRegular.replace('|', '')
            numeroEstadosF = estadoFinal + len(estadosF) +1

            estadoFinalOR = estadoFinal

            for estado_OR in estadoOR:

                for index, caracter in enumerate(estado_OR):
                    
                    if index == 0:
                        state = [estadoFinalOR, caracter, estadoFinal + 1 +estadoActual]
                    else:
                        state = [estadoFinal, caracter, estadoFinal + 1 +estadoActual]

                    estadoFinal += (1 + estadoActual)
                    if estadoActual != 0: estadoActual = 0

                    if state not in automata:
                        automata.append(state)

                    if estadoFinal not in estados:
                        estados.append(estadoFinal)

                    if index == len(estado_OR) -1:       
                        state = [estadoFinal, 'ep', numeroEstadosF]
                        if state not in automata:
                            automata.append(state)

            if star == True: 

                state = [numeroEstadosF, 'ep', estadoFinalOR]
                if state not in automata:
                    automata.append(state)

                star = False

            estadoFinal = estadoFinalOR            

            if estadoFinal not in estados:
                estados.append(estadoFinal)

        else: 

            star_states = 1

            for caracter in expresionRegular:
                state = [estadoFinal, caracter, estadoFinal +1]
                estadoFinal += 1
                star_states += 1

                if state not in automata:
                    automata.append(state)

            if star == True:
                state = [estadoFinal, 'ep', estadoAnterior]
                if state not in automata:
                    automata.append(state)

                estadoActual = star_states
                estadoFinal = estadoAnterior

    if star:
        state = [estadoFinal, 'ep', estadoAnterior]
        estadoFinal = estadoAnterior

#Funcion del epsilon closure
def epsilonClosure(estados):
    
    for state in estados:
        for estadoNFA in automata:
            if estadoNFA[0] == state and estadoNFA[1] == 'ep' and not estadoNFA[2] in estados:
                 estados.append(estadoNFA[2])
    
    return estados

#Funcion para los movimientos
def move(state,simbolo):
    temporal = []
    for s in state:
        for estadoNFA in automata:
            if estadoNFA[0] == s and estadoNFA[1] == simbolo and not estadoNFA[2] in temporal:
                temporal.append(estadoNFA[2])

    temporal = epsilonClosure(temporal)

    return temporal

#Funcion para estados nuevos
def nuevo(state,estadosNuevos):

    for n in estadosNuevos:
        if set(n) == set(state):
            return 0

    return 1

#Funcion para convertir de NFA a DFA
def NFAtoDFA(inicialNFA,finalNFA,alfabeto):

    dfa = {}
    DFA = []
    estadoActual = []
    estadosFinales = []
    estadosNuevos = []


    estadoInicial = [inicialNFA]

    estadoActual = epsilonClosure(estadoInicial)
    
    estadosNuevos.append(estadoActual)

    if finalNFA in estadoActual:
        estadosFinales.append(estadoActual)

    for state in estadosNuevos:
        for simbolo in alfabeto:

            estadoActual = move(state,simbolo)

            if estadoActual:

                if nuevo(estadoActual,estadosNuevos):
                    estadosNuevos.append(estadoActual)
                    if finalNFA in estadoActual:
                        estadosFinales.append(estadoActual)

                DFA.append([estadosNuevos.index(state),simbolo,estadosNuevos.index(estadoActual)])

    dfa["dfa"] = DFA
    dfa["estados"] = estadosNuevos
    dfa["estadosFinales"] = estadosFinales

    return dfa

#Funcion para evaluar los strings y ver si cumplen    
def evaluarEntrada(cadena, ODFA):
    dfa = ODFA["dfa"]
    ini = 0
    valid = False

    for caracter in cadena:

        found = False

        for index, state in enumerate(dfa):
            if state[0] == ini:
                if state[1] == caracter:
                    found = True
                    ini = state[2]
                    break

                
        if found == False:            
            ini = -1

                
    for final in ODFA["estadosFinales"]:
        if ini == ODFA["estados"].index(final):
            valid = True
    
    return valid


#OUTPUT A USUARIO Y LLAMADAS A FUNCIONES

print("***************EXPRESIONES REGULARES A AUTOMATAS*****************")
expresionRegular = input("Ingresa la expresión regular para la creacion de automatas:\n")
NFA(expresionRegular, False, 1)

dfa = NFAtoDFA(0, estadoFinal, alfabeto)

# Grafico
g = nx.DiGraph()
g2 = nx.DiGraph()
g.add_nodes_from(estados)

# Datos de NFA
print("NFA")
for state in automata:
    print(state)

    g.add_edge(state[0], state[2])


# Datos de DFA
print("DFA")
for a in dfa["dfa"]:
    g2.add_edge(a[0], a[2])
    print(a)

print("Estados Finales DFA:")
for final in dfa["estadosFinales"]:
    print(dfa["estados"].index(final))


nx.draw(g,with_labels=True, arrows=True)
plt.draw()
plt.show()

nx.draw(g2,with_labels=True, arrows=True)
plt.draw()
plt.show()

entradaRevision = input("¿Desea analizar un string?: (Si/No)\n")

while True:
    if entradaRevision == "Si":
        cadena = input("Ingrese la entrada a analizar\n")
        print(evaluarEntrada(cadena, dfa))
        entradaRevision = input("¿Desea analizar un nuevo string?: (Si/No)\n")

    else:
        print("Programa terminado")
        break
