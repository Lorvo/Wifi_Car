import pickle

data =  {
        "angle": 30,
        "bend": 0.004,
        "offset": 201,
        "slope": .0679,
        }

with open("settings.pkl", "wb") as f:
    pickle.dump(data, f)

with open("settings.pkl", "rb") as f:
    data = pickle.load(f)

print(data)