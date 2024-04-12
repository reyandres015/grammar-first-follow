grammar = {
    "A": [['B', "C"], ["ant",'A','all']],
    "B": [['big', "C"], ['bus','A','boss',],['ε']],
    "C": [['cat'], ['cow']]
}
nt = grammar.keys()
t = []

def identifyTerminals():
    for nont in grammar:  # Por NT de la gramatica
        for production in grammar[nont]:  # Por produccion del simbolo
            for symbol in production:
                if symbol not in nt:
                    t.append(symbol)                    

def isTerminal(s):
    return s in t


def isNonTerminal(s):
    return s in nt


def findSymbol(s):
    results = {}
    for nont in grammar:  # Por NT de la gramatica
        for production in grammar[nont]:  # Por produccion del simbolo
            for symbol in production:
                if s in production:
                    try:
                        results[nont] += [production]
                    except KeyError:
                        results[nont] = [production]
    return results

# Funcion para los primeros de un NT


def first(s):
    firsts = []
    for production in grammar[s]:  # Para cada produccion de la regla
        if (isTerminal(production[0])):
            firsts.append(production[0])
        elif (isNonTerminal(production[0])):
            firstTemp = first(production[0])
            if 'ε' in firstTemp:
                if production[1]:
                    firstTemp.remove('ε')
                    firstTemp += first(production[1])
            firsts += firstTemp
    return firsts


def follow(s):
    follows = []
    if s == next(iter(grammar)):  # Si el NT es el estado inicial, el siguiente sera $
        follows.append("$")
    # Buscamos las producciones donde se encuentra nuestro NT
    found = findSymbol(s)
    for nont in found:  # Por cada NT de las reglas encontradas
        for production in found[nont]:
            if (production.index(s) < len(production)-1):
                # El simbolo despues del NT
                nxt = production[production.index(s)+1]
                if (isTerminal(nxt)):  # Si el simbolo es terminal
                    # Agregamos ese simbolo a la lista de siguientes
                    follows.append(nxt)
                elif (isNonTerminal(nxt)):  # Si el simbolo es no terminal
                    nxt = first(nxt)  # Buscamos los primeros del siguiente
                    if ("ε" in nxt):  # Si existe epsilon en los primeros
                        # Se añaden los siguientes del padre
                        nxt += follow(nont)
                    follows += nxt
            else:
                if (s != nont):
                    follows += follow(nont)
    follows = list(set(follows))
    if ("ε" in follows):
        follows.remove("ε")
    return follows


def printGrammar():
    for rule in grammar:  # Por regla
        str_rule = rule + " -> "
        for production in grammar[rule]:  # Por produccion del no terminal
            for symbol in production:  # Por simbolo en la produccion
                str_rule += symbol
            str_rule += "|"
        str_rule = str_rule[:-1]
        print(str_rule)


def printFirsts():
    print("Primeros:")
    for nont in nt:
        print(f'P({nont}) ={first(nont)}')


def printFollows():
    print("Siguientes:")
    for nont in nt:
        print(f'S({nont}) = {follow(nont)}')


def main():
    identifyTerminals()
    print("Primeros y Siguientes de una gramatica\n")
    printGrammar()
    print("\n")
    printFirsts()
    printFollows()


main()
