import joblib
model = joblib.load(open("model.pkl", "rb"))
print(type(model))
