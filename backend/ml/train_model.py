import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ============================================
# Load Dataset
# ============================================

df = pd.read_csv("dataset.csv")

print("Dataset Loaded Successfully")
print(df.head())

# ============================================
# Remove timestamp
# ============================================

if "timestamp" in df.columns:
    df = df.drop(columns=["timestamp"])

# ============================================
# Encode categorical columns
# ============================================

label_encoders = {}

categorical_columns = [
    "sector",
    "machine",
    "shift",
    "maintenance_status",
]

for column in categorical_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(df[column])

    label_encoders[column] = encoder

# ============================================
# Target Variable
# ============================================

y = df["machine_failure"]

X = df.drop(
    columns=[
        "machine_failure",
        "fire_risk",
        "accident_risk",
    ]
)

# ============================================
# Train Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# ============================================
# Train Random Forest
# ============================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
)

model.fit(
    X_train,
    y_train,
)

# ============================================
# Evaluate
# ============================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions,
)

print("\nAccuracy:", accuracy)

print(
    classification_report(
        y_test,
        predictions,
    )
)

# ============================================
# Save Model
# ============================================

joblib.dump(
    model,
    "model.pkl",
)

joblib.dump(
    label_encoders,
    "label_encoder.pkl",
)

print("\nModel Saved Successfully")