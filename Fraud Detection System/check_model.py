import pickle

with open('fraud_detection_xgboost.pkl', 'rb') as f:
    model = pickle.load(f)

print("Expected columns:\n")
print(model.feature_names_in_)
