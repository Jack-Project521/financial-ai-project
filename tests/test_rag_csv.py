import pandas as pd
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain_chroma import Chroma
from langchain_community.document_loaders import DataFrameLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings

from common.utils.metadata_constants import DOCUMENT_CONTENT_DESCRIPTION_BEEF, \
    METADATA_FIELD_INFO_BEEF_SMALL, column_types
from common.utils.models import get_lc_model_client, OPENAI_API_KEY, OPENAI_MODEL, \
    get_embeddings_model_openai, OPENAI_EMBEDDING_MODEL_SMALL

llm = get_lc_model_client(
    OPENAI_API_KEY,
    OPENAI_MODEL,
    temperature=0,
    verbose=True
)

def test_rag_csv(user_query):

    # 关键改动 1: 定义与 AttributeInfo 匹配的数据类型字典
    # Get DataFrame by file
    try:
        docs_data_frame = pd.read_csv("../uploads/db_beef.csv", dtype=column_types)
    except FileNotFoundError:
        print("Error message：db_beef.csv can't be found!")
        return []

    # print("DataFrame Info after loading with specific dtypes: ")
    # docs_data_frame.info()

    documents = []
    for _, row in docs_data_frame.iterrows():
        # 关键改动 2: 创建一个更自然的、人类可读的 page_content
        page_content = (
            f"On the date {row['date']} (year {row['year']}, week {row['week_number']}), "
            f"the total kill number was {row['kill_number']} with a total weight of {row['kill_weight']}, total costing {row['kill_Cost_$']}, "
            f"and the kill costing per kilo {row['kill_cost_$/kg']}."
            f"The boning process involved {row['bone_number']} units with a total weight of {row['bone_weight']}, total costing {row['bone_Cost_$']}, "
            f"and the boning costing per kilo {row['bone_cost_$/kg']}."
            f"This resulted in a production of {row['prod_ctn']} cartons with a total weight of {row['prod_kg']}."
        )

        # 关键改动 3: 将每一行的原始结构化数据作为 metadata
        metadata_dict = row.to_dict()

        doc = Document(
            page_content=page_content,
            metadata=metadata_dict
        )
        documents.append(doc)

        if not documents:
            print("Can't create any documents from original file")
            return []


    vectorstore = Chroma.from_documents(documents=documents, embedding=get_embeddings_model_openai())

    document_content_description = DOCUMENT_CONTENT_DESCRIPTION_BEEF.format(columns=", ".join(docs_data_frame.columns))

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

def composite_page_content(row):
    """
    Convert one row of a DataFrame into a dictionary.
    """
    page_content = ""
    for column, value in row.items():
        # print(f"Processing current column - {column}: {value}")

        description = get_column_description(column)
        page_content += f"{description}: {value}, "
    return page_content

def get_column_description(column):
    description = ""
    metadata_field_info = METADATA_FIELD_INFO_BEEF_SMALL
    for attr in metadata_field_info:
        if attr.name == column:
            description = attr.description + " value is"
            return description

    if not description:
        description = f"the current value of {column} is"

    return description

def get_embeddings_model_openai(model=OPENAI_EMBEDDING_MODEL_SMALL):
    return OpenAIEmbeddings(model=model, api_key=OPENAI_API_KEY)

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

    # Test all data 2022 week 3
    print("what is the kill number for 2022 week 3: ", test_rag_csv("what is the kill number for 2022 week 3"))
    print("what is the bone number for 2022 week 3: ", test_rag_csv("what is the bone number for 2022 week 3"))
    print("what is the kill weight for 2022 week 3: ", test_rag_csv("what is the kill weight for 2022 week 3"))
    print("what is the bone weight for 2022 week 3: ", test_rag_csv("what is the bone weight for 2022 week 3"))
    print("what is the kill cost for 2022 week 3: ", test_rag_csv("what is the kill cost for 2022 week 3"))
    print("what is the bone cost for 2022 week 3: ", test_rag_csv("what is the bone cost for 2022 week 3"))
    print("what is the kill cost per kilo for 2022 week 3: ", test_rag_csv("what is the kill cost per kilo for 2022 week 3"))
    print("what is the bone cost per kilo for 2022 week 3: ", test_rag_csv("what is the bone cost per kilo for 2022 week 3"))
    print("what is the cartons of production for 2022 week 3: ", test_rag_csv("what is the cartons of production for 2022 week 3"))
    print("what is the weight of the carton produced for 2022 week 3: ", test_rag_csv("what is the weight of the carton produced for 2022 week 3"))







