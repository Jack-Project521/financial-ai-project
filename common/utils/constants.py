from langchain.chains.query_constructor.schema import AttributeInfo

# constants.py, Better to change and test different parameters in terms of different document types

# default top_k
DEFAULT_N_RESULTS = 5

# ------------------------------------------------------------------------- #
# -----------------------   Chunk size, overlap size  --------------------- #
# ------------------------------------------------------------------------- #

# CSV
CSV_CHUNK_SIZE = 256
CSV_CHUNK_OVERLAP = 30

# DOCX
DOCX_CHUNK_SIZE = 256
DOCX_CHUNK_OVERLAP = 30

# XLSX
XLSX_CHUNK_SIZE = 256
XLSX_CHUNK_OVERLAP = 30

# PDF
PDF_CHUNK_SIZE = 256
PDF_CHUNK_OVERLAP = 30

# DEFAULT
DEFAULT_CHUNK_SIZE = 256
DEFAULT_CHUNK_OVERLAP = 30


# ------------------------------------------------------------------------- #
# --------------------------   Prompt Templates  -------------------------- #
# ------------------------------------------------------------------------- #

# Define a prompt template for beef query
PROMPT_TEMPLATE_DEFAULT = """
    You are a great question-answering robot.
    Your task is to answer the user's question based on the known information provided below.
    Make sure your response is entirely based on the known information. 
    Do not make up answers.
    If the known information below is insufficient to answer the user's question, please 
    respond directly with "I can't answer your question.

    Known information:
    __INFO__

    User query：
    __QUERY__

    Please answer questions by English, do not answer with any questions that are not related to this database.
"""

