import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("../data/crop_dataset_full.csv")

X = data[[
    "district", "pH", "N", "P", "K",
    "avg_temp", "total_rainfall", "avg_humidity"
]]

y = data["crop"]

# Encoders
le_district = LabelEncoder()
le_crop = LabelEncoder()

X["district"] = le_district.fit_transform(X["district"])
y = le_crop.fit_transform(y)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# Save files (IMPORTANT PATHS)
pickle.dump(model, open("crop_recommendation_model.pkl", "wb"))
pickle.dump(le_district, open("crop_rec_district_encoder.pkl", "wb"))
pickle.dump(le_crop, open("crop_rec_crop_encoder.pkl", "wb"))

print("Crop recommendation model trained and saved successfully")