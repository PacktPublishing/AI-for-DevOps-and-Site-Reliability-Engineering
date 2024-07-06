import os
import argparse
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# Load the data from CSV
credit_df = pd.read_csv(
    "https://raw.githubusercontent.com/PacktPublishing/AI-for-DevOps-and-Site-Reliability-Engineering/main/Chapter13/azure-ml/default-of-credit-card-clients.csv",
    header=1,
    index_col=0,
)

# Split the data
train_df, test_df = train_test_split(
    credit_df,
    test_size=0.25,
)

# Extracting the label column
y_train = train_df.pop("default payment next month")

# Convert the dataframe values to array
X_train = train_df.values

# Extracting the label column
y_test = test_df.pop("default payment next month")

# Convert the dataframe values to array
X_test = test_df.values

# Set name for logging
mlflow.set_experiment("SRE ML Training")
# Enable autologging with MLflow
mlflow.sklearn.autolog()

# Train Gradient Boosting Classifier
print(f"Training with data of shape {X_train.shape}")
# Start logging for this model
mlflow.start_run()
# Train the model
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
clf.fit(X_train, y_train)

# Predict on test data
y_pred = clf.predict(X_test)

# Log the model
print(classification_report(y_test, y_pred))
# Stop logging for this model
mlflow.end_run()