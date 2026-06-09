from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import json

app = Flask(__name__)

# Allow frontend (5500) to access backend (5000)
CORS(app)

# Load trained ensemble model and encoders
model = pickle.load(open("model/ensemble_model.pkl", "rb"))
le_district = pickle.load(open("model/district_encoder.pkl", "rb"))
le_crop = pickle.load(open("model/crop_encoder.pkl", "rb"))

crop_rec_model = pickle.load(open("model/crop_recommendation_model.pkl", "rb"))
crop_rec_le_district = pickle.load(open("model/crop_rec_district_encoder.pkl", "rb"))
crop_rec_le_crop = pickle.load(open("model/crop_rec_crop_encoder.pkl", "rb"))

with open("model/model_metrics.json", "r") as f:
    model_metrics = json.load(f)

# Load 2025 weather data
weather = pd.read_csv("model/weather_2025_weekly.csv")
# Crop growing duration in weeks (approximate)
CROP_DURATION_WEEKS = {
    "Rice": 12,
    "Maize": 10,
    "Jowar": 12,
    "Bajra": 10,
    "Ragi": 14,
    "Red Gram": 16,
    "Bengal Gram": 14,
    "Cotton": 16,
    "Sugarcane": 48,
    "Groundnut": 14,
    "Soybean": 12,
    "Sunflower": 12,
    "Sesame": 10,
    "Chilli": 20,
    "Onion": 16
}

@app.route("/metrics", methods=["GET"])
def get_metrics():
    return jsonify(model_metrics)

@app.route("/districts", methods=["GET"])
def get_districts():
    districts = sorted(weather["district"].unique().tolist())
    return jsonify(districts)

@app.route("/crops", methods=["GET"])
def get_crops():
    crops = sorted(le_crop.classes_.tolist())
    return jsonify(crops)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        district = data["district"]
        crop = data["crop"]

        # Safety checks
        if district not in le_district.classes_:
            return jsonify({"error": "District not found in yield model"}), 400

        if crop not in le_crop.classes_:
            return jsonify({"error": "Crop not found in yield model"}), 400

        # Crop duration
        weeks = CROP_DURATION_WEEKS.get(crop, 12)

        district_weather = weather[weather["district"] == district]
        if district_weather.empty:
            return jsonify({"error": "Weather data not found"}), 400

        crop_weather = district_weather.head(weeks)

        avg_temp = crop_weather["avg_temp"].mean()
        total_rainfall = crop_weather["weekly_rainfall"].sum()
        avg_humidity = crop_weather["avg_humidity"].mean()

        # Yield prediction features
        yield_features = [[
            le_district.transform([district])[0],
            le_crop.transform([crop])[0],
            float(data["pH"]),
            float(data["N"]),
            float(data["P"]),
            float(data["K"]),
            float(avg_temp),
            float(total_rainfall),
            float(avg_humidity)
        ]]

        predicted_yield = model.predict(yield_features)[0]

        # ---- Crop Recommendation ----
        if district not in crop_rec_le_district.classes_:
            return jsonify({
                "predicted_yield": round(float(predicted_yield), 2),
                "recommended_crop": "Not available for this district"
            })

        rec_features = [[
            crop_rec_le_district.transform([district])[0],
            float(data["pH"]),
            float(data["N"]),
            float(data["P"]),
            float(data["K"]),
            float(avg_temp),
            float(total_rainfall),
            float(avg_humidity)
        ]]

        rec_index = crop_rec_model.predict(rec_features)[0]
        recommended_crop = crop_rec_le_crop.inverse_transform([rec_index])[0]

        return jsonify({
            "predicted_yield": round(float(predicted_yield), 2),
            "recommended_crop": recommended_crop
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)