import read_files
import pandas as pd
import re

def formulaWithoutNumber(dfGFA):
    #Lee el archivo de compuestos
    dfGFA= read_files.loadGFA()

    #Definir un df para guardar el resulrado
    dfCompound = pd.DataFrame(columns =['Formula', 'Phase'])

    for index,row in dfGFA.iterrows():
        formulaTx = row['Formula']
        Phase = row['Phase']
        #Seleccionar compuestos sin valores numericos
        if str.isalpha(formulaTx):
            strleng = len(formulaTx)
            for char in formulaTx:
                if char.isupper():
                    element = re.findall('[A-Z][^A-Z]*', formulaTx)
            cantComp=str(round(100/(len(element)),1))
            lisComponentsCantComponent = [x + cantComp for x in element]
            strComponentsCantComponent = ''.join([str(elem) for elem in lisComponentsCantComponent])
            dfCompound.loc[len(dfCompound)] = strComponentsCantComponent,Phase       
    return(dfCompound)
