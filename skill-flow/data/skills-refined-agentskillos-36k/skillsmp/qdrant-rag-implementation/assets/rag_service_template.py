"""
RAG Service Template
This template demonstrates proper implementation of async RAG service with Qdrant and OpenAI integration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
import logging
import os
import inspect
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str] = []
    metadata: dict = {}

class SelectionRequest(BaseModel):
    selected_text: str
    question: str

class SelectionResponse(BaseModel):
    answer: str

class RAGService:
    def __init__(self, vector_store_collection: str = "default_collection", vector_store_timeout: int = 30):
        """
        Initialize the RAG service with required components.

        Args:
            vector_store_collection: Name of the vector store collection to use
            vector_store_timeout: Timeout for vector store operations
        """
        # In a real implementation, you would configure your client here
        # For AsyncOpenAI clients, the create method is inherently async
        # self.client = external_client (from config)
        # self.model = model_config.model
        pass

    async def check_api_connection(self):
        """
        Check if the API connection is working.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # For AsyncOpenAI clients (like Qwen), the create method itself is async
            # response = await self.client.chat.completions.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are a test assistant."},
            #         {"role": "user", "content": "Test connection"}
            #     ],
            #     max_tokens=10
            # )
            # return True
            return True  # Placeholder for actual implementation
        except Exception as e:
            logging.error(f"API connection test failed: {e}")
            return False

    def check_vector_store_connection(self):
        """
        Check if the vector store connection is working.

        Returns:
            True if connection is successful, False otherwise
        """
        # Implement actual connection check with your vector store
        return True  # Placeholder

    async def check_health(self):
        """
        Check the health of both the API and vector store.

        Returns:
            Dictionary with health status of both components
        """
        try:
            api_healthy = await self.check_api_connection()
            vector_store_healthy = self.check_vector_store_connection()
            
            # Get vector store health details if available
            vector_store_details = {}
            # if self.vector_store:
            #     try:
            #         vector_store_details = self.vector_store.health_check()
            #     except Exception:
            #         vector_store_details = {"status": "unreachable"}
            
            return {
                "api_healthy": api_healthy,
                "vector_store_healthy": vector_store_healthy,
                "vector_store_details": vector_store_details,
                "status": "healthy" if api_healthy and vector_store_healthy else "unhealthy"
            }
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            return {
                "api_healthy": False,
                "vector_store_healthy": False,
                "status": "unhealthy",
                "error": str(e)
            }

    def set_vector_store(self, vector_store):
        """
        Set the vector store instance to use for retrieval.

        Args:
            vector_store: Initialized VectorStore instance
        """
        self.vector_store = vector_store

    async def query(self, query_text: str, top_k: int = 5) -> QueryResponse:
        """
        Process a query using the RAG pipeline.

        Args:
            query_text: User's question
            top_k: Number of top results to retrieve from vector store

        Returns:
            QueryResponse with answer and sources
        """
        try:
            # Validate inputs
            if not query_text or not query_text.strip():
                return QueryResponse(answer="Please provide a query", sources=[], metadata={})

            # Step 1: Generate embedding for the query
            # from data.embeddings import EmbeddingService
            # embedding_service = EmbeddingService()
            # query_embedding = embedding_service.embed_text(query_text)

            # Step 2: Verify vector store is available and retrieve relevant documents
            if not hasattr(self, 'vector_store'):
                raise ValueError("Vector store not set in RAG service")

            # Check connection before performing search
            if not self.vector_store.check_connection():
                logging.error("Vector store connection lost during query")
                return QueryResponse(answer="Service temporarily unavailable", sources=[], metadata={})
            
            # retrieved_docs = self.vector_store.search(query_embedding, limit=top_k)
            retrieved_docs = []  # Placeholder for actual implementation

            if not retrieved_docs:
                return QueryResponse(answer="I don't know", sources=[], metadata={"retrieved_docs_count": 0})

            # Step 3: Format context from retrieved documents
            context = "\n\n".join([doc["content"] for doc in retrieved_docs])
            sources = list(set([doc["doc_path"] for doc in retrieved_docs]))  # Unique sources

            # Step 4: Generate answer using API with the context
            prompt = f"""
            Context information is below:
            {context}

            Using the provided context information, answer the question: {query_text}

            If the context does not contain sufficient information to answer the question, respond with "I don't know".
            """

            # For AsyncOpenAI clients (like Qwen), the create method itself is async
            # response = await self.client.chat.completions.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided context. If the context does not contain sufficient information to answer the question, respond with 'I don't know'."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     max_tokens=500,
            #     temperature=0.1
            # )

            # For placeholder, we'll just return a sample response
            response = type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'This is a sample response based on the context.'})})]})()

            answer = response.choices[0].message.content.strip()

            # Check if the answer is "I don't know"
            if "i don't know" in answer.lower():
                return QueryResponse(answer="I don't know", sources=[], metadata={"retrieved_docs_count": len(retrieved_docs)})

            return QueryResponse(
                answer=answer, 
                sources=sources, 
                metadata={
                    "retrieved_docs_count": len(retrieved_docs),
                    "sources_count": len(sources)
                }
            )

        except Exception as e:
            logging.error(f"Error in query processing: {e}")
            return QueryResponse(
                answer="An error occurred while processing your query", 
                sources=[],
                metadata={"error": str(e)}
            )

    async def answer_from_selection(self, selected_text: str, question: str) -> SelectionResponse:
        """
        Answer a question based only on the selected text.

        Args:
            selected_text: Text selected by the user
            question: Question about the selected text

        Returns:
            SelectionResponse with answer
        """
        try:
            # Validate inputs
            if not selected_text or not selected_text.strip():
                return SelectionResponse(answer="Please provide selected text")
            if not question or not question.strip():
                return SelectionResponse(answer="Please provide a question")

            # Format the prompt using only the selected text
            prompt = f"""
            Selected text is below:
            {selected_text}

            Using only the provided selected text, answer the question: {question}

            If the selected text does not contain sufficient information to answer the question, respond with "I don't know".
            """

            # For AsyncOpenAI clients (like Qwen), the create method itself is async
            # response = await self.client.chat.completions.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided selected text. If the selected text does not contain sufficient information to answer the question, respond with 'I don't know'."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     max_tokens=500,
            #     temperature=0.1
            # )

            # For placeholder, we'll just return a sample response
            response = type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'This is a sample response based on the selected text.'})})]})()

            answer = response.choices[0].message.content.strip()

            # Check if the answer is "I don't know"
            if "i don't know" in answer.lower():
                return SelectionResponse(answer="I don't know")

            return SelectionResponse(answer=answer)

        except Exception as e:
            logging.error(f"Error in selection-based answering: {e}")
            return SelectionResponse(answer="An error occurred while processing your question")