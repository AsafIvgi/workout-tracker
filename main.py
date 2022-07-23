import requests as r
import datetime as dt
import os

exercise_text = input("Tell me which exercises you did: ")
TODAY_DATE = dt.datetime.now().strftime("%d/%m/%Y")
NOW_TIME = dt.datetime.now().strftime("%X")
GENDER = "male"
WEIGHT = 68
HEIGHT = 177
AGE = 29
NUTRIX_APP_ID = os.environ["NT_APP_ID"]
NUTRIX_API_KEY = os.environ["NT_API_KEY"]
NUTRIX_BASE_URL = "https://trackapi.nutritionix.com"
NUTRIX_EX_ENDPOINT = "v2/natural/exercise"
NUTI_HEADERS = {
    "x-app-id": NUTRIX_APP_ID,
    "x-app-key": NUTRIX_API_KEY,
    "Content-Type": "application/json"
}
PARAMS = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

SHEETY_URL = os.environ["SHEETY_ENDPOINT"]
SHEETY_HEADERS = (
    os.environ["SHEETY_USERNAME"],
    os.environ["SHEETY_PASSWORD"],
)
nuti_response = r.post(url=f"{NUTRIX_BASE_URL}/{NUTRIX_EX_ENDPOINT}", headers=NUTI_HEADERS, json=PARAMS)
result = nuti_response.json()

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": TODAY_DATE,
            "time": NOW_TIME,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheet_response = r.post(url=SHEETY_URL, json=sheet_inputs, auth=SHEETY_HEADERS)
    print(sheet_response.text)
