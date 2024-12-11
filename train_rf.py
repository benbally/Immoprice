# Insights on how we trained the Random Forest model


# Import libraries

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib


# Load the housing market dataset

dataset = "/Users/benjaminbally/desktop/usa_data.csv"
df = pd.read_csv(dataset)


# Drop any rows with missing values

df.dropna(inplace=True)


# Define independent variables (x) and dependent variable (y)

x = df[["bed", "bath", "city", "house_size"]]
y = df["price"]


# Convert city names (categorical) into numerical values

label_encoder = LabelEncoder()
x.loc[:, "city"] = label_encoder.fit_transform(x["city"])


# Split the data into training data (80%) and test data (20%)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)


# Scale independent variables

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)


# Train the Random Forest model: We are using a reduced amount of trees and a reduced max. depth for the training for storage reasons

forest = RandomForestRegressor(
    n_estimators=50,     
    max_depth=10,         
    max_features="sqrt",  
    min_samples_split=10  
)

forest.fit(x_train_scaled, y_train)


# Save the trained model, scaler, and label encoder

joblib.dump(forest, "finalizedmodel.pkl", compress=3)
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")


# Evaluate the model

forest.score(x_test_scaled, y_test)
