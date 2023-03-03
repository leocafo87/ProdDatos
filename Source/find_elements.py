import read_files
import pandas as pd
import formula_NotNumber

#Rellenar con vacios los elementos hasta completar 8, colocar la cantidad de elementos y la formula inicial
def CompleteListElements(CantElemen,IndxElements,formulaTx):
    if CantElemen < 8:
        for i in range(CantElemen,8):
            nanStr = ''
            IndxElements.append(nanStr)
    IndxElements.append(str(CantElemen))
    IndxElements.insert(0,str(formulaTx))
    return(IndxElements)
  
#Procesar los archivos de entrada
def findIndexPosition(dfGFA,dfElements):
    #Declaracion de listas vacias
    PosElement=[]
    IndxElements=[]
    IndxNextElement=[]
    LengElement=[]

    #variables temporales para ejecuciones pequeñas
    elements = {'Element':['Ca','Ag','Fe','Cu','B','Cr','Mo','C','Co','Ni','Pd']}
    formulas = {'Formula':['Ag27Cu73','Cu0.5NiAlCoCrFe','Fe30Cr30Mo15C15B10','B18.5Co81.5','[(Ni0.9Fe0.1)0.75B0.2Si0.05]96Nb4','Co20.9Pd62.6Si16.5','AlCrMoSiTi']}
    #fin de las variables temporales

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

    #Definir un df para guardar el resulrado
    dfElementsOfCompos = pd.DataFrame(columns =['Formula', 'Elem1','Elem2','Elem3','Elem4','Elem5','Elem6','Elem7','Elem8','CantElemen'])

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
        CantElemen= (len(IndxElements))  
        #llamado a la funcion CompleteListElements   
        completeList=CompleteListElements(CantElemen,IndxElements,formulaTx)
        
        #Obtener un df con todos los elementos presentes en un formula
        dfElementsOfCompos.loc[len(dfElementsOfCompos)] = completeList
        IndxElements=[]
        PosElement=[]
        IndxNextElement=[]
        LengElement=[]
    print(dfElementsOfCompos)



