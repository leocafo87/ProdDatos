import read_files
import pandas as pd
import formula_NotNumber

def findIndexPosition(dfGFA,dfElements):
    elements = {'Element':['Ca','Ag','Fe','Cu','B','Cr','Mo','C','Co']}
    formulas = {'Formula':['Ag27Cu73','Fe30Cr30Mo15C15B10','B18.5Co81.5','[(Ni0.9Fe0.1)0.75B0.2Si0.05]96Nb4','Co20.9Pd62.6Si16.5','AlCrMoSiTi']}
    temp_dfGFA= pd.DataFrame(data=formulas)
    temp_dfElements= pd.DataFrame(data=elements)

    #temp_dfGFA= read_files.loadGFA()
    dfFormula=temp_dfGFA
    #temp_dfElements = read_files.loadTablaPeriodica() 
    dfElements=temp_dfElements

    #Procesa las formulas que no tienen valores de proporcion
    dfNotNumbe = formula_NotNumber.formulaWithoutNumber(dfGFA)

    #Unir los dfs
    dfGFA = (pd.concat([dfFormula, dfNotNumbe]))
    print(dfGFA)

    PosElement=[]
    IndxElements=[]
    IndxNextElement=[]
    LengElement=[]

    for index, row in dfGFA.iterrows():
        for index, row1 in dfElements.iterrows():
            formulaTx = row['Formula']
            elementTx = row1['Element']
            posIndex = formulaTx.find(elementTx)
            lenElement = len(elementTx)
            nextSubStr = formulaTx[posIndex+lenElement:posIndex+lenElement+1]
            if posIndex >= 0 and nextSubStr.isnumeric() and not str.isalpha(formulaTx):
                PosElement.append(posIndex)                
                substr = formulaTx[posIndex:posIndex+lenElement]
                IndxElements.append(substr)
                IndxNextElement.append(nextSubStr)
                LengElement.append(lenElement)
        print(formulaTx,IndxElements)
        IndxElements=[]
        PosElement=[]
        IndxNextElement=[]
        LengElement=[]












































