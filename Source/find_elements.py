import read_files
import pandas as pd

def findIndexPosition(dfGFA,dfElements):
    elements = {'Element':['Ca','Ag','Fe','Cu','B','Cr','Mo','C']}
    formulas = {'Formula':['Ag27Cu73','Fe30Cr30Mo15C15B10','B18.5Co81.5','Cu35Ti65','Co20.9Pd62.6Si16.5','Fe30Cr30Mo15Cu15B10']}
    #formulas = {'Formula':['Ag27Cu73']}
    df= pd.DataFrame(data=formulas)
    df1= pd.DataFrame(data=elements)
    dfGFA= read_files.loadGFA()
    df=dfGFA
    dfElements = read_files.loadTablaPeriodica() 
    df1=dfElements

    PosElement=[]
    IndxElements=[]
    IndxNextElement=[]
    LengElement=[]

    for index, row in df.iterrows():
        for index, row1 in df1.iterrows():
            formulaTx = row['Formula']
            elementTx = row1['Element']
            posIndex = formulaTx.find(elementTx)
            lenElement = len(elementTx)
            nextSubStr = formulaTx[posIndex+lenElement:posIndex+lenElement+1]
            if posIndex >= 0 and nextSubStr.isnumeric():
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



