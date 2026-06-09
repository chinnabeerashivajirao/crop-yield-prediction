import json
import pandas as pd
import pickle
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import SVR
from sklearn.ensemble import StackingRegressor

data = pd.read_csv("../data/crop_dataset_full.csv")

print("Dataset shape:", data.shape)
print("Crops in training:", data["crop"].unique())

le_district = LabelEncoder()
le_crop = LabelEncoder()

data["district"] = le_district.fit_transform(data["district"])
data["crop"] = le_crop.fit_transform(data["crop"])

X = data[[
    "district","crop","pH","N","P","K",
    "avg_temp","total_rainfall","avg_humidity"
]]

y = data["yield"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

base_models = [
    ("rf", RandomForestRegressor(n_estimators=100, random_state=42)),
    ("gb", GradientBoostingRegressor(random_state=42)),
    ("lr", LinearRegression()),
    ("svr", SVR())
]

model = StackingRegressor(
    estimators=base_models,
    final_estimator=Ridge(),
    cv=5
)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print("R2 Score:", r2)
print("RMSE:", rmse)

# Save metrics
metrics = {
    "r2_score": round(float(r2), 3),
    "rmse": round(float(rmse), 3)
}

with open("model_metrics.json", "w") as f:
    json.dump(metrics, f)

pickle.dump(model, open("ensemble_model.pkl", "wb"))
pickle.dump(le_district, open("district_encoder.pkl", "wb"))
pickle.dump(le_crop, open("crop_encoder.pkl", "wb"))

print("Model trained successfully")