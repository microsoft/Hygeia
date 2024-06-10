from typing import Annotated
import logging
import os
import requests

from semantic_kernel.functions import kernel_function

class KernelMemoryPlugin:
    base_url = os.getenv("KERNEL_MEMORY_SERVICE_ENDPOINT")
    index = os.getenv("KERNEL_MEMORY_SERVICE_INDEX")
    
    @kernel_function(
        name="ask",
        description="Ask a question about indexed documents.",
    )
    def ask(
        self,
        question: Annotated[str, "the question to ask"],
    ) -> Annotated[str, "the output is a string"]:
        """Returns the response from Kernel Memory service ask"""
        # call the http endpoint to ask the question
        response = requests.post(f"{self.base_url}ask", json={"question": question, "index": self.index, "minRelevance": 0.5, "limit": 1})
        return response.text        

    @kernel_function(
        name="search",
        description="Search for indexed documents.",
    )
    def search(
        self,
        query: Annotated[str, "the search query"],
    ) -> Annotated[str, "the output is a string"]:
        """Returns the search query response."""
        response = requests.post(f"{self.base_url}search", json={"query": query, "index": self.index, "limit": 5, "minRelevance": 0.5})
        return response.text
    
    @kernel_function(
        name="upload",
        description="Upload a document to the memory.",
    )
    def upload(
        self,
        file: Annotated[bytes, "the file to upload"],
        document_id: Annotated[str, "the document id"],
        file_name: Annotated[str, "the file name"],
    ) -> Annotated[str, "the output is a string"]:
        """Returns the file upload response."""
        logging.info(f"Index name: {self.index}")

        response = requests.post(f"{self.base_url}upload", files={ file_name: file }, data={"index": self.index, "documentId": document_id})
        return response.text

    @kernel_function(
        name="deleteDocuments",
        description="Delete a document from the memory.",
    )
    def delete(
        self,        
        document_id: Annotated[str, "the document id"],
    ) -> Annotated[str, "the output is a string"]:
        """Returns the file delete response."""
        logging.info(f"Index name: {self.index}")

        response = requests.delete(f"{self.base_url}documents?index={self.index}&documentId={document_id}")

        return response.text