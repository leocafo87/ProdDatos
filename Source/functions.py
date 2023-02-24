import read_files
import pandas as pd
import re

def formulaWithoutNumber(dfGFA):
    #Definir un df para guardar el resulrado
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
        #Si el compuesto tiene parentesis al inicio y al final, pasar
        if example_compuesto.startswith('(') and example_compuesto.endswith(')'):
            #Eliminar los parentesis
            example_compuesto = example_compuesto.replace('(', '')
            example_compuesto = example_compuesto.replace(')', '')
        else:
            match = re.search(r'\((.*?)\)(\d+\.?\d*)', example_compuesto)
            compuesto = match.group(1)
            multiplicador = match.group(2)
            compuesto = re.sub(r'(\d+\.?\d*)', lambda x: str(float(x.group(1))* float(multiplicador)), compuesto)

            #Reemplazar el compuesto en la formula
            example_compuesto = example_compuesto.replace(match.group(0), compuesto)

    if example_compuesto.count('[') > 0:
        match = re.search(r'\[(.*?)\](\d+\.?\d*)', example_compuesto)
        compuesto = match.group(1)
        multiplicador = match.group(2)

        compuesto = re.sub(r'(\d+\.?\d*)', lambda x: str(float(x.group(1))* float(multiplicador)), compuesto)

        #Reemplazar el compuesto en la formula
        example_compuesto = example_compuesto.replace(match.group(0), compuesto)
    if example_compuesto.count('{') > 0:
        match = re.search(r'\{(.*?)\}(\d+\.?\d*)', example_compuesto)
        compuesto = match.group(1)
        multiplicador = match.group(2)

        compuesto = re.sub(r'(\d+\.?\d*)', lambda x: str(float(x.group(1))* float(multiplicador)), compuesto)

        #Reemplazar el compuesto en la formula
        example_compuesto = example_compuesto.replace(match.group(0), compuesto)
    
    #Separar los numeros de la formula y guardarlos en una lista
    number = re.findall(r'\d+\.?\d*', example_compuesto)
    #Guardar en una lista lo restante de la formula
    element = re.split(r'\d+\.?\d*', example_compuesto)
    #Unir las listas en un diccionario
    dict_compuesto = dict(zip(element, number))
    #Convertir el diccionario en un dataframe
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

def validateComposition(df):
    df_copy = df.copy()
    #Sumar los valores de las columnas Compo1, Compo2, etc
    for index, row in df_copy.iterrows():
        suma = 0
        for i in range(1,9):
            if row[f'Compo{i}'] != None:
                suma += float(row[f'Compo{i}'])
        df_copy.loc[index, 'Suma'] = suma

    #Intervalo de error permitido
    error = 1
    #Validar que la suma este dentro del intervalo de error
    df_copy['Validacion'] = df_copy['Suma'].apply(lambda x: True if x >= 100-error and x <= 100+error else False)
    return df_copy

def generateReport(df):
    #Eliminar la columna Validacion y Suma
    df_report = df.drop(['Validacion', 'Suma'], axis=1)
    #Guardar el reporte en un archivo csv
    df_report.to_csv("../Outputs/Report.csv", index=False)
    print('Se generó correctamente el reporte')
    return df_report