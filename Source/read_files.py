import os
import pandas as pd

def loadGFA():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../Inputs/GFADataset.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    df_GFA = pd.read_csv(filename, sep=",")
    dfGFA=df_GFA.rename(columns={"Alloy Formula":"Formula","Phase Formation":"Phase"})
    return dfGFA
    #print(dfGFA)

def loadTablaPeriodica():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../Inputs/TablaPeriodica.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    df_Tabla = pd.read_csv(filename, sep=";")
    df_TablaPeriodica=df_Tabla.rename(columns={"Eea (ev)":"Eea(ev)","I1 (ev)":"I1(ev)","I2 (ev)":"I2(ev)","Tm (K)":"Tm(K)","Rm (nm)":"Rm(nm)","Rc (nm)":"Rc(nm)","Cp (J/molK)":"Cp(J/molK)","K (W/m)/K 300K":"K(W/m)/K300K","Hf (kJ/mol)":"Hf(kJ/mol)","Tb (K)":"Tb(K)"})
    return df_TablaPeriodica
    #print(df_Tabla)

def loadErroresModelo():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../Inputs/ErroresModelo.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    df_ErroresModelo = pd.read_csv(filename, sep=";")
    return df_ErroresModelo
    #print(df_ErroresModelo)