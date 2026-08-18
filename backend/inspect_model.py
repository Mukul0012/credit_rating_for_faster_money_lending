import joblib

MODEL_PATH = (
    "app/ml/models/random_forest_tuned.pkl"
)

model = joblib.load(MODEL_PATH)

print("=" * 60)
print("MODEL TYPE")
print("=" * 60)

print(type(model))


print("\n" + "=" * 60)
print("MODEL")
print("=" * 60)

print(model)


print("\n" + "=" * 60)
print("N FEATURES")
print("=" * 60)

print(
    getattr(
        model,
        "n_features_in_",
        "Not available"
    )
)


print("\n" + "=" * 60)
print("FEATURE NAMES")
print("=" * 60)

print(
    getattr(
        model,
        "feature_names_in_",
        "Not available"
    )
)


print("\n" + "=" * 60)
print("CLASSES")
print("=" * 60)

print(
    getattr(
        model,
        "classes_",
        "Not available"
    )
)


print("\n" + "=" * 60)
print("PARAMETERS")
print("=" * 60)

print(model.get_params())