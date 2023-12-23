from unittest.mock import Mock, patch

import pytest

from app.utils.files import UnstructuredFileInterpreter, file_loader_factory


def test_file_loader_factory_unstructured():
    with patch("app.config") as mock_config:
        mock_config.__getitem__.return_value = "unstructured"
        loader = file_loader_factory()
        assert isinstance(loader, UnstructuredFileInterpreter)

def test_file_loader_factory_unsupported():
    with patch("app.config") as mock_config:
        mock_config.__getitem__.return_value = "unsupported"
        with pytest.raises(ValueError):
            file_loader_factory()

def test_unstructured_file_interpreter_parse_pdf():
    with patch("app.utils.files.UnstructuredPDFLoader") as mock_loader_class:
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = ["document"]
        mock_loader_class.return_value = mock_loader_instance

        interpreter = UnstructuredFileInterpreter()
        interpreter.parse("file.pdf")

        assert interpreter.documents == ["document"]
        assert interpreter.key == "file.pdf"

def test_unstructured_file_interpreter_parse_img():
    with patch("app.utils.files.UnstructuredImageLoader") as mock_loader_class:
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = ["document"]
        mock_loader_class.return_value = mock_loader_instance

        interpreter = UnstructuredFileInterpreter()
        interpreter.parse("file.png")

        assert interpreter.documents == ["document"]
        assert interpreter.key == "file.png"

def test_unstructured_file_interpreter_process():
    with patch("app.utils.files.UnstructuredFileInterpreter.parse") as mock_parse, \
         patch("app.utils.db") as mock_db:
        mock_db_instance = Mock()
        mock_db.save.return_value = None
        mock_db.return_value = mock_db_instance

        interpreter = UnstructuredFileInterpreter()
        interpreter.process("file.pdf", mock_db)

        mock_parse.assert_called_once_with("file.pdf")
        mock_db.save.assert_called_once_with(interpreter.documents, "file.pdf")

def test_unstructured_file_interpreter_simple_file_type():
    interpreter = UnstructuredFileInterpreter()
    assert interpreter.simple_file_type("file.pdf") == UnstructuredFileInterpreter.FileType.PDF
    assert interpreter.simple_file_type("file.png") == UnstructuredFileInterpreter.FileType.PNG
