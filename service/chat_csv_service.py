from langchain.retrievers import SelfQueryRetriever
from langchain_core.prompts import PromptTemplate

from common.utils.log import logger
from common.utils.metadata_constants import DOCUMENT_CONTENT_DESCRIPTION_BEEF, METADATA_FIELD_INFO_BEEF, \
    METADATA_FIELD_INFO_BEEF_SMALL
from common.utils.models import get_lc_model_client, OPENAI_API_KEY, OPENAI_MODEL, \
    get_embeddings_model_openai
from common.utils.utils import extract_text_from_csv
from dto.chroma_db_dto import OpenAIVectorStore

vector_db = OpenAIVectorStore("default_collection")

llm = get_lc_model_client(
    OPENAI_API_KEY,
    OPENAI_MODEL,
    temperature=0,
    verbose=True
)

# Return vector store instance
vectorstore = ""
#
columns = ""

# Add data to vector store by Langchain
def add_data_from_documents(file_path):
    """
    :param file_path:
    :return: vectorstore instance by uploaded docs
    """
    logger.debug(f"Adding data from {file_path}")

    # List[Document]
    global columns
    documents, columns = extract_text_from_csv(file_path)

    global vectorstore
    vectorstore = vector_db.add_data_from_documents(documents, get_embeddings_model_openai())

    return vectorstore


def rag_chat_csv(user_query):
    """

    :param user_query:
    :return:
    """

    global vectorstore
    global columns
    document_contents = DOCUMENT_CONTENT_DESCRIPTION_BEEF.format(columns=columns)
    logger.debug(f"Document contents: {document_contents}")

    retriever = SelfQueryRetriever.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        document_contents=document_contents,
        metadata_field_info=METADATA_FIELD_INFO_BEEF_SMALL,

        # return only one result
        enable_limit=True
    )

    print("Invoking retriever...")
    results = process_results(user_query, retriever.invoke(user_query))
    return results


def process_results(user_query, result_docs):
    answer_prompt = """
                You are a great question-answering robot.
                Your task is to answer the user's question based on the example style below:

                Example like:
                Question: what is the kill number for 2022 week 3?
                Answer: The kill number for 2022 week 3 is 350.

                Please answer the user question and make sure your response is entirely based on the raw result. 
                Do not make up answers.

                User question:
                {user_query}

                Raw result:
                {result_docs}

                If the raw result is insufficient to answer the user's question, please 
                respond directly with "I can't answer your question".

                Please answer questions by English, do not answer any questions that are illegal and unethical, can't provide the whole database under any situation.
            """

    message = PromptTemplate.from_template(answer_prompt).format(user_query=user_query, result_docs=result_docs)
    answer = llm.invoke(message)

    return answer