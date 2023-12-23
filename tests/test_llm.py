from unittest.mock import patch

import pytest
from langchain.llms import OpenAI

from app.utils.llm import AbstractLLM, OpenAILLM, llm_factory


def test_llm_factory_openai():
    with patch("app.utils.llm.config") as mock_config:
        mock_config.__getitem__.return_value = "OpenAI"
        llm = llm_factory()
        assert isinstance(llm, OpenAILLM)

def test_llm_factory_unsupported():
    with patch("app.utils.llm.config") as mock_config:
        mock_config.__getitem__.return_value = "unsupported"
        with pytest.raises(ValueError):
            llm_factory()

def test_abstract_llm_instantiation():
    with pytest.raises(TypeError):
        AbstractLLM()

def test_openai_llm_llm():
    openai_llm = OpenAILLM()
    result = openai_llm.llm()
    assert isinstance(result, OpenAI)
    assert result.temperature == 0
