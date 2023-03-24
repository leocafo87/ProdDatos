
def load_data():
    import pandas as pd
    import os
    df = pd.read_csv("../model/total_data.csv")

    y = df["Phase"]
    x = df.drop(columns=["Phase"])
    return x, y

def make_train_test_split(x, y):

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

def eval_metrics(y_true, y_pred):

    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return mse, mae, r2

def report(estimator, mse, mae, r2):

    print(estimator, ":", sep="")
    print(f"  MSE: {mse}")
    print(f"  MAE: {mae}")
    print(f"  R2: {r2}")

def run():
    #
    # Entrena un modelo sklearn ElasticNet
    #
    import sys
    from sklearn.ensemble import RandomForestClassifier
    import mlflow


    x, y = load_data()
    x_train, x_test, y_train, y_test = make_train_test_split(x, y)

    n_estimators = float(sys.argv[1])
    max_depth = float(sys.argv[2])
    verbose = int(sys.argv[3])

    print('Tracking directory:', mlflow.get_tracking_uri())

    with mlflow.start_run():
        estimator = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        estimator.fit(x_train, y_train)
        mse, mae, r2 = eval_metrics(y_test, y_pred=estimator.predict(x_test))
        if verbose > 0:
            report(estimator, mse, mae, r2)

        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)

        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(estimator, "model")

if __name__ == "__main__":
    run()