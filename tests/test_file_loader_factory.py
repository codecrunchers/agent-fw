import pytest
from unittest.mock import patch, Mock
from app import (
    file_loader_factory,
    UnstructuredFileInterpreter,
)


# Test for file_loader_factory
def test_file_loader_factory_unstructured():
    with patch("app.utils.config.AbstractConfig.get") as mock_config:
        mock_config.return_value = {"file_loader_type": "unstructured"}
        loader = file_loader_factory()
        assert isinstance(loader, UnstructuredFileInterpreter)


def test_file_loader_factory_unsupported_type():
    with patch("app.utils.config.AbstractConfig.get") as mock_config:
        mock_config.return_value = {"file_loader_type": "unsupported"}
        with pytest.raises(ValueError):
            file_loader_factory()


# Test for UnstructuredFileInterpreter
@pytest.mark.asyncio
async def test_unstructured_file_interpreter_parse():
    test_uri = "some_test_uri"
    expected_output = "expected_output"

    with patch("app.UnstructuredPDFLoader") as mock_loader_class:
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [expected_output]
        mock_loader_class.return_value = mock_loader_instance

        interpreter = UnstructuredFileInterpreter()
        result = await interpreter.parse(test_uri)

        assert result == expected_output
        mock_loader_class.assert_called_with(test_uri)
        mock_loader_instance.load.assert_called_once()
