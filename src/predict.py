import joblib
import pandas as pd

def predict(file_path):
    data = pd.read_csv(file_path)

    # Load the model artifacts using joblib
    artifacts = joblib.load("src/artifacts.joblib")

    # Unpack the artifacts
    numerical_features = artifacts["features"]["numerical_features"]
    categorical_features = artifacts["features"]["categorical_features"]
    enc = artifacts["enc"]
    model = artifacts["model"]

    # Apply imputer and encoder on data
    data_cat = enc.transform(data[categorical_features]).toarray()
    data = pd.concat(
        [
            data[numerical_features].reset_index(drop=True),
            pd.DataFrame(data_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )
    # Make predictions
    predictions = model.predict(data)
    return predictions.tolist()
