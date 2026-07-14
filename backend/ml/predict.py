import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
encoders = joblib.load(os.path.join(BASE_DIR, "label_encoder.pkl"))


def safe_encode(name, value):
    """
    Encode categorical value.
    If value wasn't present during training,
    use the first known class instead.
    """

    encoder = encoders[name]

    if value not in encoder.classes_:
        value = encoder.classes_[0]

    return encoder.transform([value])[0]


def predict_failure(
    sector,
    machine,
    shift,
    temperature,
    pressure,
    gas_co,
    gas_co2,
    oxygen,
    vibration,
    humidity,
    smoke_level,
    noise_level,
    motor_rpm,
    bearing_temperature,
    power_consumption,
    oil_level,
    workers_present,
    maintenance_status,
    risk_score,
    failure_probability,
    maintenance_due_days,
):

    sector = safe_encode("sector", sector)
    machine = safe_encode("machine", machine)
    shift = safe_encode("shift", shift)
    maintenance_status = safe_encode(
        "maintenance_status",
        maintenance_status,
    )

    df = pd.DataFrame([{
        "sector": sector,
        "machine": machine,
        "shift": shift,
        "temperature": temperature,
        "pressure": pressure,
        "gas_co": gas_co,
        "gas_co2": gas_co2,
        "oxygen": oxygen,
        "vibration": vibration,
        "humidity": humidity,
        "smoke_level": smoke_level,
        "noise_level": noise_level,
        "motor_rpm": motor_rpm,
        "bearing_temperature": bearing_temperature,
        "power_consumption": power_consumption,
        "oil_level": oil_level,
        "workers_present": workers_present,
        "maintenance_status": maintenance_status,
        "risk_score": risk_score,
        "failure_probability": failure_probability,
        "maintenance_due_days": maintenance_due_days,
    }])

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "prediction": int(prediction),
        "probability": round(float(probability), 4),
    }