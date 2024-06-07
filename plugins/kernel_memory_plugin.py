import io
from typing import Annotated
import http
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
        response = requests.post(f"{self.base_url}ask", json={"question": question, "index": self.index})
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
        response = requests.post(f"{self.base_url}search", json={"query": query, "index": self.index})
        return response.text
    
    @kernel_function(
        name="upload",
        description="Upload a document to the memory.",
    )
    def upload(
        self,
        file: Annotated[io.BytesIO, "the file to upload"],
        document_id: Annotated[str, "the document id"],
    ) -> Annotated[str, "the output is a string"]:
<<<<<<< HEAD
        """Returns the file upload response."""
        response = requests.post(f"{self.base_url}upload", files={"file1": file}, data={"index": self.index, "documentId": document_id})
        return response.text
=======
        """Returns the file upload response."""        
        response = requests.post(f"{self.base_url}upload", json={"documentId": file, "index": self.index})
        return "upload response"
>>>>>>> origin/JT1343-1344-IndexDocs
