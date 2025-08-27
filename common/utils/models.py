import inspect
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# models.py
# Provide different LLMs list, and instances of them, also some encapsulation
# Constants including model tpye, model API_KEY, base url, embedding models



# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY");
OPENAI_MODEL = "gpt-4.1";
OPENAI_URL = "https://api.openai.com/v1"
# For most implementations, text-embedding-3-small with 512 dimensions provides the best balance of performance and cost efficiency
OPENAI_EMBEDDING_MODEL_SMALL= "text-embedding-3-small"
# Only when you need state-of-the-art accuracy for complex semantic tasks.
OPENAI_EMBEDDING_MODEL_LARGE= "text-embedding-3-large"

# Default embedding model
DEFAULT_EMBEDDING_MODEL_BGE = "BAAI/bge-m3";


# Create the client object of certain platform by using langchain, default platform is OpenAI
def get_lc_model_client(api_key=OPENAI_API_KEY,
                        model=OPENAI_MODEL,
                        base_url=OPENAI_URL,
                        temperature=0,
                        verbose=False, debug=False):

    """
    Get the certain platform by Langchain
    verbose, debug two parameters control whether output the debugging information and the detailed debugging information respectively, do not print as default

    :param api_key:
    :param base_url:
    :param model:
    :param temperature:
    :param verbose:
    :param debug:
    :return: platform instance of Langchain
    """

    function_name = inspect.currentframe().f_code.co_name
    if verbose:
        print(f"{function_name} -- platform: {base_url}, model: {model}, temperature: {temperature}")
    if debug:
        print(f"{function_name} -- platform: {base_url}, model: {model}, temperature: {temperature}, api_key: {api_key}")

    return ChatOpenAI(api_key=api_key,
                      model=model,
                      base_url=base_url,
                      temperature=temperature)

# Provide embedding result by embedding model - bge‑m3
def get_embeddings_bge(texts, model=DEFAULT_EMBEDDING_MODEL_BGE):

    """

    :param texts: list of documents - list[str]
    :param model:
    :return: list[list[float]]
    """
    embeddings = HuggingFaceEmbeddings(model_name=model)
    return embeddings.embed_documents(texts)

# Provide embedding result by embedding model - OPENAI
def get_embeddings_openai(texts, model=OPENAI_EMBEDDING_MODEL_SMALL):

    """

    :param texts: list of documents - list[str]
    :param model:
    :return: list[list[float]]
    """
    embeddings = get_embeddings_model_openai(model=model)
    return embeddings.embed_documents(texts)

# Get instance only of OpenAIEmbeddings
def get_embeddings_model_openai(model=OPENAI_EMBEDDING_MODEL_SMALL):
    return OpenAIEmbeddings(model=model, api_key=OPENAI_API_KEY)