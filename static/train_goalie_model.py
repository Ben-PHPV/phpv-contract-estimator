import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. Load your goalie contract data
df = pd.read_csv("data/updated_goalies_contracts.csv")

# 2. Pick the columns that matter
df = df.drop_duplicates(subset="name")
df = df[[
    "games_played", "xGoals", "Age", "IsRFA", "YL", "Length", "ContractAAV"
]].dropna()

X = df.drop("ContractAAV", axis=1)  # input columns
y = df["ContractAAV"]               # output (what we're trying to predict)

# 3. Train the model
model = RandomForestRegressor()
model.fit(X, y)

# 4. Save the trained model to a file
joblib.dump(model, "goalie_model.pkl")
