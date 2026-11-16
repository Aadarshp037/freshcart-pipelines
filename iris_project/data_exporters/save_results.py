
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import os


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Export Iris model predictions to CSV.
    """

    predictions = data['predictions']
    actual = data['y_test']

    results = pd.DataFrame({
        'actual': actual.to_numpy(),
        'predicted': predictions
    })

    output_file = 'iris_predictions.csv'
    results.to_csv(output_file, index=False)

    print("Predictions saved:", os.path.abspath(output_file))
    print("Total predictions:", len(results))

    return os.path.abspath(output_file)


@test
def test_output(output, *args):
    assert output is not None
    assert os.path.exists(output)
    assert os.path.getsize(output) > 0
