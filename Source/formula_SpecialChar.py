import read_files
import pandas as pd
import re

#Procesar formulas que empiezan con caracteres epseciales
def FormulaStarSpecialChar(dfGFA):
    dfGFA= read_files.loadGFA()

    #Para cada formula que comience con caracteres diferentes a letras
    #se tratara de cumplir el estandar de formulas definidas

    #isinstance(s, str)

    for index,row in dfGFA.iterrows():
        formulaTx = row['Formula']
        Phase = row['Phase']
        
        formulaTx=formulaTx.replace("{","(")
        formulaTx=formulaTx.replace("[","(")
        formulaTx=formulaTx.replace("}",")")
        formulaTx=formulaTx.replace("]",")")

        # Definir una expresión regular para buscar elementos y sus composiciones en la fórmula.
        #patron = r"([A-Z][a-z]*)(\d*(?:\.\d+)?)|(\()|(\))(\d*(?:\.\d+)?)"
        patronElementos = r"([A-Z][a-z]*)"
        patronNumeros = r"(\d*(?:\.\d+)?)|(\()|(\))(\d*(?:\.\d+)?)"
        # Buscar todos los elementos y sus composiciones en la fórmula.
        
        if not formulaTx[0].isalpha():
            elementos = re.findall(patronElementos, formulaTx)
            elementosNros = re.findall(str(patronNumeros), formulaTx)
            print(formulaTx)
            print(elementos)
            print(elementosNros)