
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Load dataset
iris = load_iris(as_frame=True)
df = iris.frame
print("1. Dataset loaded:", df.shape)

# 2. Prepare data
train_df, test_df = train_test_split(
    df, test_size=0.2, random_state=42
)

X_train = train_df.drop(columns=["target"])
y_train = train_df["target"]

X_test = test_df.drop(columns=["target"])
y_test = test_df["target"]

print("2. Training rows:", len(X_train))
print("   Testing rows:", len(X_test))

# 3. Train and test different depths
results = []

for depth in [1, 2, 3, 4, 5]:
    model = DecisionTreeClassifier(
        max_depth=depth, random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    results.append({
        "max_depth": depth,
        "test_accuracy": accuracy
    })

    print(f"Depth {depth}: Accuracy = {accuracy:.4f}")

# 4. Final model
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# 5. Save predictions
output = pd.DataFrame({
    "actual": y_test.to_numpy(),
    "predicted": predictions
})

output.to_csv("iris_predictions.csv", index=False)

# 6. Evaluation
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nAccuracy comparison:")
print(pd.DataFrame(results).to_string(index=False))

# 7. Tests
assert len(df) == 150
assert len(X_train) == 120
assert len(X_test) == 30
assert len(predictions) == 30
assert 0 <= accuracy_score(y_test, predictions) <= 1
assert pd.read_csv("iris_predictions.csv").shape[0] == 30

print("\nALL PIPELINE TESTS PASSED")
print("Predictions saved to iris_predictions.csv")
