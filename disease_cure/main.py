import json

def get_disease_info(data, disease_name):
    for disease in data["diseases"]:

        if disease["name"] == disease_name:
            cause = ", ".join(disease["cause"])
            prevention = ", ".join(disease["prevention"])
            cure = ", ".join(disease["cure"])
            pesticide = disease["pesticide"]

            info = [
            {"Disease Name": disease_name},
            {"Cause": cause},
            {"Prevention": f"To prevent this disease. {prevention}"},
            {"Cure": cure},
            {"Pesticide": f"{pesticide} can be used to cure this disease"}
            ]
            return info

    return f"Disease '{disease_name}' not found."
