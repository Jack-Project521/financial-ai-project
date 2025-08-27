import json

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader, UnstructuredExcelLoader, PyPDFLoader, Docx2txtLoader, \
    CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from common.utils.constants import CSV_CHUNK_SIZE, CSV_CHUNK_OVERLAP, XLSX_CHUNK_SIZE, XLSX_CHUNK_OVERLAP, \
    PDF_CHUNK_SIZE, PDF_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from common.utils.log import logger
from common.utils.metadata_constants import METADATA_FIELD_INFO_BEEF_SMALL, column_types
from common.utils.models import get_lc_model_client, OPENAI_API_KEY, OPENAI_MODEL


# Reading and extracting .doc, .docx file
def extract_text_from_docx(file):

    """
    Extracting text from docx file
    :param file:
    :return: list[str] - A list of text chunks obtained after splitting from uploaded file
    """
    full_text = ""

    # Open and read doc
    loader = Docx2txtLoader(file)

    documents = loader.load()

    # Get a list of text chunks obtained after splitting
    chunks = chunk_doc_documents(CSV_CHUNK_SIZE, CSV_CHUNK_OVERLAP, documents)
    print("chunks: ", chunks)
    return documents

# RAG friendly
# Reading and extracting .csv file by DataFrameLoader
# Chunked by RecursiveCharacterTextSplitter
def extract_text_from_csv(file):

    # Get DataFrame by file
    try:
        docs_data_frame = pd.read_csv(file, dtype=column_types)
    except FileNotFoundError:
        logger.error(f"File {file} not found!")
        return []

    # Merge all columns into one string per row
    docs_data_frame["merged"] = docs_data_frame.apply(composite_page_content, axis=1)

    # Get list[Document]
    loader = DataFrameLoader(docs_data_frame, page_content_column="merged")
    documents = loader.load()

    logger.debug(f"documents: {documents}")

    return documents, ", ".join(docs_data_frame.columns)

# Composite page_content with NLP
def composite_page_content(row):
    """
    Convert one row of a DataFrame into a NLP string.
    """
    page_content = (
        f"On the date {row['date']} (year {row['year']}, week {row['week_number']}), "
        f"the total kill number was {row['kill_number']} with a total weight of {row['kill_weight']}, total costing {row['kill_Cost_$']}, "
        f"and the kill costing per kilo {row['kill_cost_$/kg']}."
        f"The boning process involved {row['bone_number']} units with a total weight of {row['bone_weight']}, total costing {row['bone_Cost_$']}, "
        f"and the boning costing per kilo {row['bone_cost_$/kg']}."
        f"This resulted in a production of {row['prod_ctn']} cartons with a total weight of {row['prod_kg']}."
    )
    return page_content

# Reading and extracting .xls, .xlsx
def extract_text_from_excel(file):

    """
    Reading and extracting .xls, .xlsx
    :param file:
    :return: list[str]
    """

    # Load excel
    loader = UnstructuredExcelLoader(file, mode="elements", strategy="fast")

    documents = loader.load()

    # Chunking
    chunks = chunk_doc_documents(XLSX_CHUNK_SIZE, XLSX_CHUNK_OVERLAP, documents);
    print("chunks: ", chunks)

    return chunks

# Reading and extracting .pdf file
def extract_text_from_pdf(file):

    """
    Extracting text from pdf file
    :param file:
    :return: list[str]
    """

    # Load pdf
    loader = PyPDFLoader(file)
    # Get list[Document]
    documents = loader.load()

    # Chunking, final list[str] of chunks
    chunks = chunk_doc_documents(PDF_CHUNK_SIZE, PDF_CHUNK_OVERLAP, documents)
    print("chunks: ", chunks)

    return chunks

# Chunking function - deal with str
def chunk_doc_text(chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP, full_text=""):
    """
    Split the input text into smaller chunks based on predefined separators
    :param chunk_size:
    :param chunk_overlap:
    :param full_text:
    :return: A list of text chunks obtained after splitting
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(full_text)

# Chunking function - deal with list[Document]
def chunk_doc_documents(chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP, documents=None):
    """
    Split the input list[Document] into smaller chunks based on predefined separators
    :param chunk_size:
    :param chunk_overlap:
    :param documents: list[Document]
    :return: list[str]
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    return [chunk.page_content for chunk in chunks]

# Support .csv, .docx, doc, pdf, excel
# Add doc to vector store by parameter collection name given - here is original doc name like collection_name.doc
def prepare_documents(file_path):
    print('-' * 100)
    print("Adding document file_path: ", file_path)


    # Validate the file, read its content
    documents = ""

    if file_path.endswith(".docx") or file_path.endswith(".doc"):
        # Read the doc
        documents = extract_text_from_docx(file_path)

    # if file_path.endswith(".csv"):
    #     documents = extract_text_one_liner_chunked_from_csv(file_path)

    if file_path.endswith(".xls") or file_path.endswith(".xlsx"):
        documents = extract_text_from_excel(file_path)

    if file_path.endswith(".pdf"):
        documents = extract_text_from_pdf(file_path)

    if not documents:
        return "It is an empty document!"

    return documents

# Build prompt from template, prepared for the use of LLM retrieval-augmented part
def build_prompt_from_template(prompt_template, **kwargs):

    # Get the prompt template str
    prompt = prompt_template

    # Replacing placeholders by real values
    for key, value in kwargs.items():

        #
        if isinstance(value, str):
            val = value

            # Check if value is list type, then check all elements in it whether its str
            # Join every str element to one str - val
        elif isinstance(value, list) and all(isinstance(e, str) for e in value):
            val = "\n".join(value)

        else:
            # Force casting value to str
            val = str(value)

        # Must keep the placeholder name the same as the keys passed
        prompt = prompt.replace(f"__{key.upper()}__", val)

    return prompt

# Get completion from LLM, namely, give response from LLM after asking questions by prompts
def get_completion(prompt):
    chat_client = get_lc_model_client(
        OPENAI_API_KEY,
        OPENAI_MODEL,
        temperature=0,
        verbose=True
    )
    return chat_client.invoke(prompt)