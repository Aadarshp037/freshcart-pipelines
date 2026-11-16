
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


@transformer
def transform(data, *args, **kwargs):
    """
    Train a Decision Tree classifier on the prepared Iris dataset.
    """

    # Get max_depth from runtime variables
    max_depth = kwargs.get('max_depth', 3)

    # Separate training and testing records
    train_df = data[data['split'] == 'train']
    test_df = data[data['split'] == 'test']

    # Separate features and target
    feature_cols = [
        col for col in data.columns
        if col not in ['target', 'split']
    ]

    X_train = train_df[feature_cols]
    y_train = train_df['target']

    X_test = test_df[feature_cols]
    y_test = test_df['target']

    # Train Decision Tree
    model = DecisionTreeClassifier(
        max_depth=int(max_depth),
        random_state=42
    )

    model.fit(X_train, y_train)

    # Generate predictions
    predictions = model.predict(X_test)

    # Calculate test accuracy
    accuracy = accuracy_score(y_test, predictions)

    print("Max depth:", max_depth)
    print("Test accuracy:", accuracy)

    return {
        'model': model,
        'predictions': predictions,
        'y_test': y_test,
        'X_test': X_test,
        'test_accuracy': accuracy,
        'max_depth': int(max_depth)
    }


@test
def test_output(output, *args):
    assert output is not None
    assert 'test_accuracy' in output
    assert output['test_accuracy'] >= 0.80, (
        f"Model accuracy too low: {output['test_accuracy']}"
    )
