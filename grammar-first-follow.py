# -*- coding: utf-8 -*-
"""
    Primeros y Siguientes de una gramatica en Python
    - Luis David Arias
"""

t = ["+","-","*","/","ε","id","num","(",")"]
nt = ["E","E'","T","T'","f"]
grammar = {
"E":[("T","E'")],
"E'":[("+","T","E'"),("-","T","E'"),("ε",)],
"T":[("f","T'")],
"T'":[("*","f","T'"),("/","f","T'"),("ε",)],
"f":[("(","E",")"),("id",),("num",)]
}

def isTerminal(s):
    return s in t

def isNonTerminal(s):
    return s in nt

def findSymbol(s):
    results = {}
    for nont in grammar:#Por NT de la gramatica
        for production in grammar[nont]:#Por produccion del simbolo
            for symbol in production:
                if s in production:
                    try:
                        results[nont]+=[production]
                    except KeyError:
                        results[nont]=[production]
    return results

#Funcion para los primeros de un NT
def first(s):
    firsts = []
    for production in grammar[s]:#Para cada produccion de la regla
        #print("Analizamos la produccion "+str(production))
        if(isTerminal(production[0])):
            #print(production[0]+" es terminal")
            firsts.append(production[0])
        elif(isNonTerminal(production[0])):
            #print(production[0]+" es no terminal")
            firsts+=first(production[0])
    return firsts

def follow(s):
    follows = []
    if s == next(iter(grammar)):#Si el NT es el estado inicial, el siguiente sera $
        follows.append("$")
    found = findSymbol(s)#Buscamos las producciones donde se encuentra nuestro NT
    for nont in found:#Por cada NT de las reglas encontradas
        for production in found[nont]:
            if(production.index(s) < len(production)-1):
                nxt = production[production.index(s)+1]#El simbolo despues del NT
                if(isTerminal(nxt)):#Si el simbolo es terminal
                    follows.append(nxt)#Agregamos ese simbolo a la lista de siguientes
                elif(isNonTerminal(nxt)):#Si el simbolo es no terminal
                    nxt = first(nxt)#Buscamos los primeros del siguiente
                    if("ε" in nxt):#Si existe epsilon en los primeros
                        nxt += follow(nont)#Se añaden los siguientes del padre
                    follows+= nxt
            else:
                if(s != nont):
                    follows = follow(nont)
    follows = list(set(follows))
    if("ε" in follows):
        follows.remove("ε")
    return follows

def printGrammar():
    for rule in grammar:#Por regla
        str_rule = rule + " -> "
        for production in grammar[rule]:#Por produccion del no terminal
            for symbol in production:#Por simbolo en la produccion
                str_rule+=symbol
            str_rule+="|"
        str_rule = str_rule[:-1]
        print(str_rule)

def printFirsts():
    print("Primeros:")
    for nont in nt:
        print(first(nont))

def printFollows():
    print("Siguientes:")
    for nont in nt:
        print(follow(nont))


def main():
    print("Primeros y Siguientes de una gramatica\n")
    printGrammar()
    print("\n")
    printFirsts()
    printFollows()

main()
