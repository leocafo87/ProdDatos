import pandas as pd
import re
import numpy as np


def separar_formula(formula):
    """
    Toma una fórmula química y la separa en elementos y sus composiciones.
    Devuelve un diccionario que contiene los elementos y sus cantidades.
    """
    formula=formula.replace("{","(")
    formula=formula.replace("[","(")
    formula=formula.replace("}",")")
    formula=formula.replace("]",")")
    # Definir una expresión regular para buscar elementos y sus composiciones en la fórmula.
    patron = r"([A-Z][a-z]*)(\d*(?:\.\d+)?)|(\()|(\))(\d*(?:\.\d+)?)"
    
    # Buscar todos los elementos y sus composiciones en la fórmula.
    elementos = re.findall(patron, formula)
    
    # Crear una pila para guardar los elementos y sus composiciones mientras se analiza la fórmula.
    pila = []
    
    # Iterar sobre cada elemento encontrado en la fórmula.
    for elemento, cantidad, parentesis_abierto, parentesis_cerrado, cantidad_parentesis in elementos:
        if elemento != "":
            # Si se encuentra un elemento, agregarlo a la pila con su cantidad correspondiente.
            if cantidad == "":
                cantidad = "1"
            pila.append({elemento: float(cantidad)})
        elif parentesis_abierto != "":
            # Si se encuentra un paréntesis abierto, agregar una nueva pila vacía.
            pila.append([])
        elif parentesis_cerrado != "":
            # Si se encuentra un paréntesis cerrado, calcular la composición dentro del paréntesis
            # y agregarla a la pila anterior. Luego, multiplicar la composición por la cantidad
            # especificada después del paréntesis cerrado (si existe).
            sub_composicion = {}
            while True:
                # Sacar elementos de la pila actual hasta encontrar el paréntesis abierto correspondiente.
                elem = pila.pop()
                if isinstance(elem, dict):
                    for k, v in elem.items():
                        if k in sub_composicion:
                            sub_composicion[k] += v
                        else:
                            sub_composicion[k] = v
                else:
                    break
            sub_cantidad = 1.0
            if cantidad_parentesis != "":
                sub_cantidad = float(cantidad_parentesis)
            for k, v in sub_composicion.items():
                sub_composicion[k] = v * sub_cantidad
            pila.append(sub_composicion)
            #pila[-1].append(sub_composicion)
    
    for i in range(len(pila)):
    #if(len(pila)>1):
      pila[0].update(pila[i])
    # Convert object to a list
    data = list(pila[0].values())
    # Convert list to an array
    numpyArray = np.array(data)
    total=sum(numpyArray)
    resultado=pila[0]
    #base 100
    for key,value in resultado.items():
      resultado[key]=value/total*100
    
    # La pila resultante debe tener un solo elemento (el diccionario de composición completo).
    # Extraer este elemento de la pila y devolverlo.
    return resultado#pila.pop()[0]
