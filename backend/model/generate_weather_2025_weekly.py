import pandas as pd
import random

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

data = []

for district in districts:
    for week in range(1, 53):

        # Seasonal logic
        if week <= 8:  # Winter
            temp = random.uniform(20, 26)
            rain = random.uniform(0, 10)
            humidity = random.uniform(45, 60)

        elif week <= 20:  # Summer
            temp = random.uniform(30, 42)
            rain = random.uniform(0, 15)
            humidity = random.uniform(30, 45)

        elif week <= 40:  # Monsoon
            temp = random.uniform(26, 34)
            rain = random.uniform(20, 80)
            humidity = random.uniform(60, 85)

        else:  # Post-monsoon
            temp = random.uniform(22, 30)
            rain = random.uniform(5, 20)
            humidity = random.uniform(50, 65)

        data.append([
            district,
            week,
            round(temp, 1),
            round(rain, 1),
            round(humidity, 1)
        ])

df = pd.DataFrame(
    data,
    columns=[
        "district",
        "week",
        "avg_temp",
        "weekly_rainfall",
        "avg_humidity"
    ]
)

df.to_csv("weather_2025_weekly.csv", index=False)

print("✅ weather_2025_weekly.csv generated successfully!")