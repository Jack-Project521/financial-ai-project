import chromadb
from langchain_chroma import Chroma

from common.utils.models import get_embeddings_bge, get_embeddings_openai


class OpenAIVectorStore:

    def __init__(self, collection_name):

        # Persist in disk
        self.chroma_client = chromadb.PersistentClient(path="./openai_chroma")

        # Create a default collection
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    # Add documents and vector with collection name given
    def add_documents_by_collection_name(self, documents, collection_name):
        print('add_documents: collection_name:', collection_name)

        # Create a collection by parameter: collection_name
        collection = self.chroma_client.get_or_create_collection(name=collection_name)

        # Add documents chunked and vectors into collection
        # Embedding through batch process
        batch_size = 10
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i: i + batch_size]

            collection.add(
                embeddings=get_embeddings_openai(batch_docs),
                # The vector to every document (every batch_size chunks)
                documents=batch_docs,  # Original docs contents
                ids=[f"id{i}" for i in range(i, i + len(batch_docs))]  # The ID to every document
            )

    # Retrieval of vector store by collection name given
    def search_by_collection_name(self, query, collection_name, n_results):
        print('search: collection_name:', collection_name)

        # Create local collection by name
        collection = self.chroma_client.get_or_create_collection(name=collection_name)

        # Retrieving vector store
        results = collection.query(
            query_embeddings=get_embeddings_openai([query]),
            n_results=n_results
        )

        return results

    # Add data to vector store by Langchain, return vector store instance
    def add_data_from_documents(self, documents, embeddings_model):
        """

        :param documents:
        :param embeddings_model:
        :return: vector store instance based on documents
        """
        print("-" * 100)
        print("Execute langchain_chroma.vectorstores.Chroma.from_documents to add documents into db.")
        print("-" * 100)
        return Chroma.from_documents(persist_directory="./openai_chromadb", documents=documents, embedding=embeddings_model)