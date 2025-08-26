import pandas as pd
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain_chroma import Chroma
from langchain_community.document_loaders import DataFrameLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings

from common.utils.metadata_constants import DOCUMENT_CONTENT_DESCRIPTION_BEEF, METADATA_FIELD_INFO_BEEF, \
    METADATA_FIELD_INFO_BEEF_SMALL
from common.utils.models import get_lc_model_client, OPENAI_API_KEY, OPENAI_MODEL, \
    get_embeddings_model_openai, OPENAI_EMBEDDING_MODEL_SMALL
from common.utils.utils import extract_text_from_csv
from dto.chroma_db_dto import OpenAIVectorStore

vector_db = OpenAIVectorStore("default_collection")

llm = get_lc_model_client(
    OPENAI_API_KEY,
    OPENAI_MODEL,
    temperature=0,
    debug=True
)

def query_csv(question: str):

    df = pd.read_csv("../uploads/db_beef.csv")

    template = """
    You are a Python Pandas expert.
    I have a DataFrame `df` with the following columns:
    {columns}

    User question: {question}

    Write Python Pandas code (do not include imports or df definition) 
    that extracts the answer from the DataFrame.
    Always assign the final answer to a variable named `result`.
    Only return code, no explanation.
    """
    prompt = PromptTemplate(input_variables=["columns", "question"], template=template)

    # 4. LLM produce Pandas codes
    code_prompt = prompt.format(columns=", ".join(df.columns), question=question)
    code = llm.invoke(code_prompt).content.strip("` \n")

    # ---- clean the output ----
    # Drop Markdown code symbols ```python ... ```
    code = code.replace("```python", "").replace("```", "").strip()
    # Drop "python" keyword
    if code.startswith("python"):
        code = code[len("python"):].strip()

    print("Cleaned code:\n", code)

    # 5. Execute Pandas code
    local_vars = {"df": df}
    exec(code, {}, local_vars)  # Run codes LLM produced
    result = local_vars.get("result", None)

    # 6. Give results to LLM then response NLP as final output
    answer_prompt = f"User question: {question}\nRaw result: {result}\nExplain the result clearly in natural language."
    answer = llm.invoke(answer_prompt).content

    return answer


def test_rag_csv(user_query):

    # Get DataFrame by file
    documents, columns = extract_text_from_csv("../uploads/db_beef.csv")

    vectorstore = vector_db.add_data_from_documents(documents, get_embeddings_model_openai())

    document_content_description = DOCUMENT_CONTENT_DESCRIPTION_BEEF.format(columns=columns)

    retriever = SelfQueryRetriever.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        document_contents=document_content_description,
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
    answer = llm.invoke(message).content

    return answer

if __name__ == "__main__":
    # print("What is the kill number for year 2022 week 20: ", query_csv("What is the kill number for year 2022 week 20"))
    # print("-"*100)
    # print("What is the kill weight for year 2022 week 13: ", query_csv("What is the kill weight for year 2022 week 13"))
    # print("-"*100)
    #
    # print("what is the kill number for 2022 week 12: ", query_csv("what is the kill number for 2022 week 12"))
    # print("-" * 100)
    # print("What is the prod_kg for year 2022 week 13: ", query_csv("What is the prod_kg for year 2022 week 13"))
    # print("-" * 100)
    # print("what is the kill number for 2022 week 3: ", query_csv("what is the kill number for 2022 week 3"))

    print("what is the kill number for 2022 week 3: ", test_rag_csv("what is the kill number for 2022 week 3"))

    print("what is the bone_weight for 2023 week 0: ", test_rag_csv("what is the bone_weight for 2023 week 0: "))
    print("what is the cartons of production for 2023 week 1: ", test_rag_csv("what is the cartons of production for 2023 week 1: "))
    print("what is the kill cost per kilo for 2023 week 2: ", test_rag_csv("what is the kill cost per kilo for 2023 week 2: "))
