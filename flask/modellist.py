def load_data():
    import pandas as pd
    import os
    df = pd.read_csv("../model/total_data.csv")

    y = df["Phase"]
    x = df.drop(columns=["Phase"])
    return x, y

def make_train_test_split(x, y):
    import pandas as pd
    import os
    
    
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    

    (x_train, x_test, y_train, y_test) = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=123456,
    )

    X_train = x_train.apply(pd.to_numeric, errors='coerce')
    X_test = x_test.apply(pd.to_numeric, errors='coerce')
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_train_scaled = pd.DataFrame(X_train_scaled).fillna(0)
    X_test_scaled = pd.DataFrame(X_test_scaled).fillna(0)


    return X_train_scaled, X_test_scaled, y_train, y_test

def devolver_phase(alloys):
    import os
    import pandas as pd
    import re 
    import simulator
    import mlflow
    from sklearn.preprocessing import StandardScaler

    mlflow.set_tracking_uri('sqlite:///mlruns.db')
    totalx, totaly = load_data()
    totalx_train, totalx_test, totaly_train, totaly_test = make_train_test_split(totalx, totaly)
    d = {'Formula': [alloys,alloys],'Phase':['CRA','BMG']}
    df=pd.DataFrame(data=d)
    print(df)
    df=simulator.clean_data(df)
    #Leer el archivo de "TablaPeriodica.csv"
    df_tabla_periodica = pd.read_csv("../Inputs/TablaPeriodica.csv", sep=";")
    for i in range(1, 9):
        df[f"Elem{i}"]=df[f'Elem{i}'].astype(object)
        # Realizar el "merge" entre df1 y df2 en función de las columnas de elementos
        df =df.merge(df_tabla_periodica, left_on=f"Elem{i}", right_on="Element", how="left")
    print('Cantidad de registros:', len(df))
    print('Cantidad de columnas:', len(df.columns))
    #Eliminar las columnas que no se necesitan
    df = df.drop(columns=["Elem1", "Elem2", "Elem3", "Elem4", "Elem5", "Elem6", "Elem7", "Elem8","Element_x", "Formula", "CantElemen"])
    df_total = df.copy()
    #Tipos de la columna "Phase"
    #Reemplazar BMG por 0, RMG por 1 y CRA por 2
    df_total["Phase"] = df_total["Phase"].replace({"BMG": 0, "RMG": 1, "CRA": 2})
    #Tipos de la columna "Phase"
    print(df_total["Phase"].unique())
    y = df_total["Phase"]
    #Las características de las columnas
    X = df_total.drop(columns=["Phase"])
    from sklearn.model_selection import train_test_split
    #Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.5)
    print(X_test)
    X_train = X_train.apply(pd.to_numeric, errors='coerce')
    X_test = X_test.apply(pd.to_numeric, errors='coerce')
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(totalx_train)
    X_test_scaled = scaler.transform(X_test)
    X_train_scaled = pd.DataFrame(X_train_scaled).fillna(0)
    X_test_scaled = pd.DataFrame(X_test_scaled).fillna(0)
    #X_train_scaled = scaler.fit_transform(X_train_scaled)
    #X_test_scaled = scaler.transform(X_test_scaled)
    model_name = "Phase"
    model_version = 1
    model = mlflow.pyfunc.load_model(
        model_uri=f"models:/{model_name}/{model_version}"
    )
    final=model.predict(X_test_scaled)

    df2=pd.DataFrame(final,columns=["Phase"])
    df2["Phase"] = df2["Phase"].replace({0:"BMG", 1:"RMG", 2:"CRA"})
    return df2.loc[0,'Phase']
