from common.utils.constants import PROMPT_TEMPLATE_DEFAULT, DEFAULT_N_RESULTS
from common.utils.utils import build_prompt_from_template, get_completion, prepare_documents
from dto.chroma_db_dto import OpenAIVectorStore

# ------------------------------------------------------------------------- #
# --------------   1. Build vector store by uploaded files  --------------- #
# ------------------------------------------------------------------------- #

vector_db = OpenAIVectorStore("default_collection")

# Add doc to vector store by parameter collection name given - here is original doc name like collection_name.doc
def save_docs_to_db(file_path, collection_name="default_collection"):

    # Get collection name
    print("Adding document to collection_name: ", collection_name)

    # Get doc by file
    documents = prepare_documents(file_path)

    # Save it in vector store
    vector_db.add_documents_by_collection_name(documents, collection_name=collection_name)


# ------------------------------------------------------------------------- #
# ------------------------------   2. Chat    ----------------------------- #
# ------------------------------------------------------------------------- #

# The whole RAG chat process, Retrieve vector store -> get top5 docs -> LLM -> Answer
def rag_chat(user_query, collection_name="default_collection", n_results=DEFAULT_N_RESULTS):
    print("-" * 100)
    print("Retrieving doc collection_name:", collection_name)

    # 1. Retrival process
    search_results = vector_db.search_by_collection_name(user_query, collection_name=collection_name, n_results=n_results)
    print('search_results:', search_results)
    print('-' * 100)
    print('search_results.get("documents"):', search_results.get("documents"))

    # 2. Build prompt augmented
    prompt = build_prompt_from_template(
        PROMPT_TEMPLATE_DEFAULT,
        # the keys words: info, query must be the same as the ones in prompt_template: __INFO__, __QUERY__ (see the definition)
        info=search_results.get("documents")[0],
        query=user_query
    )

    # 3. Invoke LLM chat and get answers
    response = get_completion(prompt)
    print("response:", response)
    return response;