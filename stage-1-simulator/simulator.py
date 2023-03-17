import os
import pandas as pd
import re 

def loadGFA():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../Inputs/GFADataset.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    dfGFA = pd.read_csv(filename, sep=",")
    return dfGFA

def loadTablaPeriodica():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../Inputs/TablaPeriodica.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    df_Tabla = pd.read_csv(filename, sep=";")
    df_TablaPeriodica=df_Tabla.rename(columns={"Eea (ev)":"Eea(ev)","I1 (ev)":"I1(ev)","I2 (ev)":"I2(ev)","Tm (K)":"Tm(K)","Rm (nm)":"Rm(nm)","Rc (nm)":"Rc(nm)","Cp (J/molK)":"Cp(J/molK)","K (W/m)/K 300K":"K(W/m)/K300K","Hf (kJ/mol)":"Hf(kJ/mol)","Tb (K)":"Tb(K)"})
    return df_TablaPeriodica


def process_next_batches(batch):
    #Convertir la lista de lotes a enteros
    dfElements = loadTablaPeriodica()
    for i in batch:
        process_next_batch(int(i))


def formulaWithoutNumber(dfGFA):
    #Definimos un df para guardar el resulrado
    dfCompound = pd.DataFrame(columns =['Formula', 'Phase'])
    #Para cada copuesto en el archivo que solo tenga caracteres, se hace la separacion por elementos
    # y se divide 100 entre la cantidad de elementos encontrados
    for index,row in dfGFA.iterrows():
        formulaTx = row['Formula']
        Phase = row['Phase']
        #Seleccionar compuestos sin valores numericos
        if str.isalpha(formulaTx):
            for char in formulaTx:
                if char.isupper():
                    element = re.findall('[A-Z][^A-Z]*', formulaTx)
            cantComp=str(round(100/(len(element)),1))
            lisComponentsCantComponent = [x + cantComp for x in element]
            strComponentsCantComponent = ''.join([str(elem) for elem in lisComponentsCantComponent])
            dfCompound.loc[len(dfCompound)] = strComponentsCantComponent,Phase       
    return(dfCompound)

def findCompositionPercentage(example_compuesto):
    if example_compuesto.count('(') > 0:
        if example_compuesto.startswith('(') and example_compuesto.endswith(')'):
            #Eliminamos los parentesis
            example_compuesto = example_compuesto.replace('(', '')
            example_compuesto = example_compuesto.replace(')', '')
        else:
            match = re.search(r'\((.*?)\)(\d+\.?\d*)', example_compuesto)
            compuesto = match.group(1)
            multiplicador = match.group(2)
            compuesto = re.sub(r'(\d+\.?\d*)', lambda x: str(float(x.group(1))* float(multiplicador)), compuesto)

            #Reemplazamos el compuesto en la formula
            example_compuesto = example_compuesto.replace(match.group(0), compuesto)

    if example_compuesto.count('[') > 0:
        match = re.search(r'\[(.*?)\](\d+\.?\d*)', example_compuesto)
        compuesto = match.group(1)
        multiplicador = match.group(2)

        compuesto = re.sub(r'(\d+\.?\d*)', lambda x: str(float(x.group(1))* float(multiplicador)), compuesto)

        #Reemplazamos el compuesto en la formula
        example_compuesto = example_compuesto.replace(match.group(0), compuesto)
    if example_compuesto.count('{') > 0:
        match = re.search(r'\{(.*?)\}(\d+\.?\d*)', example_compuesto)
        compuesto = match.group(1)
        multiplicador = match.group(2)

        compuesto = re.sub(r'(\d+\.?\d*)', lambda x: str(float(x.group(1))* float(multiplicador)), compuesto)

        #Reemplazamos el compuesto en la formula
        example_compuesto = example_compuesto.replace(match.group(0), compuesto)
    
    #Separaramos los numeros de la formula y guardarlos en una lista
    number = re.findall(r'\d+\.?\d*', example_compuesto)
    #Guardamos en una lista lo restante de la formula
    element = re.split(r'\d+\.?\d*', example_compuesto)
    #Unimos las listas en un diccionario
    dict_compuesto = dict(zip(element, number))
    #Convertimos el diccionario en un dataframe
    return dict_compuesto

def addElementsAndCompositionPercentage(df):
    for index, row in df.iterrows():
        formula = row['Formula']
        #Aplicar la funcion para encontrar el porcentaje de composicion correcto de cada elemento
        composicion = findCompositionPercentage(formula)
        for i in range(len(composicion)):
            #Agregar la key a la columna Elem{i} y el valor a la columna Compo{i}
            df.loc[index, f'Elem{i+1}'] = list(composicion.keys())[i]
            df.loc[index, f'Compo{i+1}'] = list(composicion.values())[i]
            
    #Reemplazar los valores NaN por 0
    df.fillna(0, inplace=True)
    return df

def countElements(dfGFA):
    #Contar la cantidad de elementos que tiene cada compuesto
    for index, row in dfGFA.iterrows():
        count = 0
        for i in range(1,9):
            if row[f'Elem{i}'] != 0:
                count += 1
        dfGFA.loc[index, 'CantElemen'] = count
    return dfGFA

def clean_data(dfGFA):
    #Procesa las formulas que no tienen valores de proporcion
    dfNotNumbe = formulaWithoutNumber(dfGFA)
    #Concatenar los dfs
    dfGFA = (pd.concat([dfGFA, dfNotNumbe]))
    #Concatear algunas columnas nuevas
    dfElementsOfCompos = pd.concat([dfGFA, pd.DataFrame(columns=['Elem1','Elem2','Elem3','Elem4','Elem5','Elem6','Elem7','Elem8','CantElemen','Compo1','Compo2','Compo3','Compo4','Compo5','Compo6','Compo7','Compo8'])])    
    dfGFA = addElementsAndCompositionPercentage (dfElementsOfCompos)
    dfGFA = countElements(dfGFA)
    return dfGFA

def save_consolidated_data(dfGFA, batch_number):
    #Eliminamos las columnas que no se van a utilizar, phase y batch
    dfGFA.drop(['state', 'batch'], axis=1, inplace=True)
    dfGFA.to_csv(f'../batches/batch_{batch_number}.csv', index=False)
    print('Se ha generado el reporte del lote', batch_number)


def process_next_batch(batch_number):
    dfGFA = loadGFA()
    #Tomamos el lote correspondiente
    dfGFA = dfGFA[dfGFA['batch'] == batch_number]
    dfGFA = clean_data(dfGFA)
    dfGFA = save_consolidated_data(dfGFA, batch_number)


def restart():
    #Eliminar los registros de la carpeta batches
    for file in os.listdir('../batches'):
        os.remove(os.path.join('../batches', file))
    for file in os.listdir('../reports'):
        os.remove(os.path.join('../reports', file))

    #Cambiar el estado de los registros a 'No Procesado'
    main_df = loadGFA()
    main_df['state'] = 'No Procesado'
    main_df.to_csv('../Inputs/GFADataset.csv', index=False)
    print('Se ha restablecido la simulacion')
    print('*****************************************************')
    print('Bienvenidos a la simulacion')
    print('Hay a disposicion 20 lotes de compuestos quimicos')
    print('****************************************************')
    print('Para empezar la simulacion, ejecute el siguiente comando:\n python advance.py <lote>, \n el valor maximo es 20, \n si no digita un valor, se ejecutaran todos los lotes, \n si desea ejecutar mas de un lote, digite los lotes separados por comas')
    
    