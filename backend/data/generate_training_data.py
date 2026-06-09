import pandas as pd
import random

# All 33 Telangana districts
districts = [
    "Adilabad","Bhadradri Kothagudem","Hanumakonda","Hyderabad",
    "Jagtial","Jangaon","Jayashankar Bhupalpally","Jogulamba Gadwal",
    "Kamareddy","Karimnagar","Khammam","Komaram Bheem Asifabad",
    "Mahabubabad","Mahabubnagar","Mancherial","Medak",
    "Medchal Malkajgiri","Mulugu","Nagarkurnool","Nalgonda",
    "Narayanpet","Nirmal","Nizamabad","Peddapalli",
    "Rajanna Sircilla","Rangareddy","Sangareddy","Siddipet",
    "Suryapet","Vikarabad","Wanaparthy","Warangal",
    "Yadadri Bhuvanagiri"
]

# All major Telangana crops
print("DEBUG: Using 14-crop generator")
crops = [
    "Rice", "Maize", "Jowar", "Bajra", "Ragi",
    "Red Gram", "Bengal Gram",
    "Cotton", "Sugarcane",
    "Groundnut", "Soybean", "Sunflower", "Sesame",
    "Chilli", "Onion"
]
print("Crops used:", crops)
data = []

# Generate 5000 rows (important)
for _ in range(5000):

    district = random.choice(districts)
    crop = random.choice(crops)

    pH = round(random.uniform(5.0, 7.5), 1)
    N = random.randint(20, 180)
    P = random.randint(20, 80)
    K = random.randint(20, 80)

    avg_temp = random.uniform(22, 38)
    total_rainfall = random.uniform(200, 900)
    avg_humidity = random.uniform(40, 85)

    base_yield = {
        "Rice": 3.5,
        "Maize": 3.0,
        "Jowar": 2.0,
        "Bajra": 1.8,
        "Ragi": 1.6,
        "Red Gram": 1.2,
        "Bengal Gram": 1.3,
        "Cotton": 2.5,
        "Sugarcane": 65,
        "Groundnut": 2.0,
        "Soybean": 2.2,
        "Sunflower": 1.8,
        "Sesame": 1.0,
        "Chilli": 2.0,
        "Onion": 25
    }

    base = base_yield[crop]

    yield_value = (
        base +
        (N * 0.01) +
        (P * 0.005) +
        (K * 0.004) +
        (total_rainfall * 0.001) -
        abs(avg_temp - 30) * 0.05 +
        random.uniform(-0.5, 0.5)
    )

    data.append([
        district, crop, pH, N, P, K,
        avg_temp, total_rainfall, avg_humidity,
        round(yield_value, 2)
    ])

df = pd.DataFrame(data, columns=[
    "district","crop","pH","N","P","K",
    "avg_temp","total_rainfall","avg_humidity",
    "yield"
])

df.to_csv("crop_dataset_full.csv", index=False)

print("Dataset generated successfully!")
print("Total rows:", len(df))