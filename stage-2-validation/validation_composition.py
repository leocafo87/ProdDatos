import os
import pandas as pd
    


def main():
    #Cantidad de archivos de la carpeta batches
    path = '../batches'
    files = os.listdir(path)
    bad_composition = pd.DataFrame()
    for file in files:
        lote_df = pd.read_csv(f'../batches/{file}')
        lote_df = validate_composition(lote_df)
        #Revisar si algún registro tiene False en la columna validation
        file = file.split('.')[0]
        if lote_df[lote_df['validation'] == False].any().any():
            lote_df = lote_df[lote_df['validation'] == False]
            bad_composition = pd.concat([bad_composition, lote_df])
            lote_df.to_csv(f'../reports/{file}_bad_composition.csv', index=False)
            print('El lote', file, 'tiene composiciones erroneas')
            print('Se ha generado el reporte de composiciones erroneas del lote', file)
        else:
            print('El lote', file, 'no tiene composiciones erroneas')
            


def validate_composition(df):
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
    df_copy['validation'] = df_copy['Suma'].apply(lambda x: True if x >= 100-error and x <= 100+error else False)
    return df_copy

main()