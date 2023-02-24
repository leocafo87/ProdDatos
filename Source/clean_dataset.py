import read_files
import pandas as pd
from functions import *
#Procesar los archivos de entrada
def cleanDataset(dfGFA,dfElements):
    #Procesa las formulas que no tienen valores de proporcion
    dfNotNumbe = formulaWithoutNumber(dfGFA) #FUNCIONA
    #Unir los dfs
    dfGFA = (pd.concat([dfGFA, dfNotNumbe]))
    #Concatear al dfGFA el dfElements, las columnas 'Formula', 'Elem1','Elem2','Elem3','Elem4','Elem5','Elem6','Elem7','Elem8','CantElemen', Compo1, Compo2, Compo3, Compo4, Compo5, Compo6, Compo7, Compo8
    dfElementsOfCompos = pd.concat([dfGFA, pd.DataFrame(columns=['Elem1','Elem2','Elem3','Elem4','Elem5','Elem6','Elem7','Elem8','CantElemen','Compo1','Compo2','Compo3','Compo4','Compo5','Compo6','Compo7','Compo8'])])    
    #Aplicar la función addCompositionPercentage 
    dfGFA= addElementsAndCompositionPercentage (dfElementsOfCompos)
    dfGFA = validateComposition(dfGFA)
    dfGFA = generateReport(dfGFA)
    return dfGFA

