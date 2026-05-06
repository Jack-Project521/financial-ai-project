import re
import time

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.retrievers import SelfQueryRetriever
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

from common.utils.log import logger
from common.utils.metadata_constants import DOCUMENT_CONTENT_DESCRIPTION_BEEF, METADATA_FIELD_INFO_BEEF_SMALL, \
    DOCUMENT_CONTENT_DESCRIPTION_BEEF_COLUMNS
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

# Add data to vector store by Langchain
def add_data_from_documents(file_path):
    """
    :param file_path:
    :return: vectorstore instance by uploaded docs
    """
    logger.debug(f"Adding data from {file_path}")

    # List[Document]
    documents = extract_text_from_csv(file_path)

    vector_db.add_data_from_documents(documents, get_embeddings_model_openai())



def rag_chat_csv(user_query):
    """
    :param user_query:
    :return: Generator yielding streaming chunks or complete AIMessage if streaming not requested
    """
    logger.debug(f"Invoking CSV agent with query: {user_query}")
    agent_executor = create_csv_agent_executor()
    
    # Stream events from the agent
    for event in agent_executor.stream({"input": user_query}):
        yield event


def rag_chat_csv_complete(user_query):
    """
    Non-streaming version that returns complete response.
    
    :param user_query:
    :return: AIMessage with complete response
    """
    logger.debug(f"Invoking CSV agent with query: {user_query}")
    agent_executor = create_csv_agent_executor()
    response = agent_executor.invoke({"input": user_query})
    return AIMessage(content=response.get("output", "I can't answer your question"))


def stream_rag_chat_csv(user_query):
    """
    Stream CSV agent response for real-time output.
    Yields formatted chunks suitable for Server-Sent Events or streaming responses.
    
    :param user_query: User's query
    :return: Generator yielding text chunks
    """
    logger.debug(f"Streaming CSV agent with query: {user_query}")
    agent_executor = create_csv_agent_executor()
    
    buffer = ""
    for event in agent_executor.stream({"input": user_query}):
        # Extract text from LLM token events - no use currently
        # if "messages" in event:
        #     for message in event["messages"]:
        #         if hasattr(message, "content") and isinstance(message.content, str):
        #             buffer += message.content
                    #yield message.content
        
        # Extract final output
        if "output" in event:
            output = event["output"]
            if isinstance(output, str):
                words = output.split()  
                for word in words:
                    yield f" {word} \n\n" # space + word
                    time.sleep(0.1)  # simulate LLM latency

def create_csv_agent_executor():
    tools = [retrieve_csv_data]
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            You are a CSV data agent for beef statistics.

            Answer the user's question in English using only data returned by the
            retrieve_csv_data tool. Always call retrieve_csv_data before answering.

            If the tool result is insufficient, answer exactly:
            I can't answer your question

            Do not make up answers. Do not provide the whole database under any situation.
            Do not answer questions that are illegal or unethical.
        """),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    print("Agent created successfully")
    return AgentExecutor(agent=agent, tools=tools, verbose=True)



@tool
def retrieve_csv_data(user_query: str) -> str:
    """
    Search the uploaded beef statistics CSV data for rows relevant to the user's question.

    Use this tool for questions about date, year, week_number, kill_number, bone_number,
    kill_weight, bone_weight, kill_Cost_$, bone_Cost_$, kill_cost_$/kg, bone_cost_$/kg,
    prod_ctn, or prod_kg. The tool returns only the retrieved CSV rows and metadata.
    """
    document_contents = DOCUMENT_CONTENT_DESCRIPTION_BEEF.format(columns=DOCUMENT_CONTENT_DESCRIPTION_BEEF_COLUMNS)
    logger.debug(f"Document contents: {document_contents}")

    vectorstore = vector_db.reconnect_vectorstore(get_embeddings_model_openai())
    retriever = SelfQueryRetriever.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        document_contents=document_contents,
        metadata_field_info=METADATA_FIELD_INFO_BEEF_SMALL,

        # return only one result
        enable_limit=True
    )

    logger.debug("Invoking CSV retriever tool")
    return process_results(user_query, retriever.invoke(user_query))

def process_results(user_query, result_docs):
    if not result_docs:
        return "I can't answer your question"

    formatted_results = []
    for index, doc in enumerate(result_docs, start=1):
        formatted_results.append(
            f"metadata: {doc.metadata}\n"
            f"content: {doc.page_content}"
        )

    return "\n\n".join(formatted_results)
