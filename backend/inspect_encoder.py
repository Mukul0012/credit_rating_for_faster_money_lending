import joblib

ENCODER_PATH = "app/ml/models/encoder.pkl"

encoder = joblib.load(
    ENCODER_PATH
)

print("=" * 60)
print("ENCODER TYPE")
print("=" * 60)

print(type(encoder))

print("\n" + "=" * 60)
print("FEATURE NAMES IN")
print("=" * 60)

print(
    getattr(
        encoder,
        "feature_names_in_",
        "Not available"
    )
)

print("\n" + "=" * 60)
print("CATEGORIES")
print("=" * 60)

print(
    getattr(
        encoder,
        "categories_",
        "Not available"
    )
)

print("\n" + "=" * 60)
print("FEATURE NAMES OUT")
print("=" * 60)

try:

    print(
        encoder.get_feature_names_out()
    )

except Exception as e:

    print("Could not get feature names:")
    print(e)