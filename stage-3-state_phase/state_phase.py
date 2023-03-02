import os
import pandas as pd
import time


def main():
    #Cantidad de archivos de la carpeta batches

    bad_compositions = read_reports()
    consolid_report = read_batches(bad_compositions)
    consolid_report = select_phase(consolid_report)
    #save_final_report(consolid_report)


def loadGFA():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../Inputs/GFADataset.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    dfGFA = pd.read_csv(filename, sep=",")
    return dfGFA

def read_reports():
    report_path = '../reports'
    report_files = os.listdir(report_path)
    bad_compositions = []
    for report in report_files:
        report_1= report.split('_')[0]
        report_2= report.split('_')[1]
        report_complete = report_1 + '_' + report_2 + '.csv'
        bad_compositions.append(report_complete)
    
    print(f'Los siguientes lotes tienen composiciones erroneas: {bad_compositions} no se tendran en cuenta para el analisis de fase')

    return bad_compositions    

def read_batches(bad_compositions):
    path = '../batches'
    files = os.listdir(path)
    consolid_report = pd.DataFrame()
    for file in files:
        if file in bad_compositions:
            continue
        else:
            df = pd.read_csv(path + '/' + file)
            #Concatear los dataframes
            consolid_report = pd.concat([consolid_report, df])
    return consolid_report


def select_phase(consolid_report):
    print('Los ingenieros estan trabajando en la selección de la fase')
    for i in range(5):
        print('...')
        time.sleep(1)
    print('Los ingenieros han terminado de seleccionar la fase')

    consolid_report = change_state(consolid_report)

    return consolid_report


def change_state(consolid_report):
    index_list = consolid_report['index'].tolist()
    df_main = loadGFA()
    #Tomar los indices de los registros que se van a cambiar
    for index in index_list:
        df_main.loc[index, 'state'] = 'Procesado'

    print('Se ha cambiado el estado de los registros a Procesado')
    #Actualizar el archivo GFADataset.csv
    df_main.to_csv('../Inputs/GFADataset.csv', index=False)
    print('Se ha actualizado el archivo GFADataset.csv')
    return consolid_report


def save_final_report(consolid_report):
    consolid_report.to_csv('../reports/final_report.csv', index=False)
    print('Se ha guardado el reporte consolidado final en la carpeta reports')

main()