
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from sklearn.datasets import load_iris


@data_loader
def load_iris_data(*args, **kwargs):
    """
    Load the Iris dataset as a pandas DataFrame.
    """
    iris = load_iris(as_frame=True)
    df = iris.frame

    return df


@test
def test_output(output, *args) -> None:
    """
    Validate the loaded Iris dataset.
    """
    assert output is not None
    assert len(output) == 150
    assert output.isnull().sum().sum() == 0
    assert output['target'].nunique() == 3
