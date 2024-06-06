import asyncio
from typing import Annotated

from semantic_kernel.functions import kernel_function

class KernelMemoryPlugin:
    
    @kernel_function(
        name="ask",
        description="Ask a question about indexed documents.",
    )
    def ask(
        self,
        question: Annotated[str, "the question to ask"],
    ) -> Annotated[str, "the output is a string"]:
        """Returns the response from Kernel Memory service ask"""
        # do the stuff here
        # return the response
        return "ask response"

    @kernel_function(
        name="search",
        description="Search for indexed documents.",
    )
    def search(
        self,
        query: Annotated[str, "the search query"],
    ) -> Annotated[str, "the output is a string"]:
        """Returns the search query response."""
        return "search response"
    
    @kernel_function(
        name="upload",
        description="Upload a document to the memory.",
    )
    def upload(
        self,
        file: Annotated[str, "the file to upload"],
    ) -> Annotated[str, "the output is a string"]:
        """Returns the file upload response."""        
        return "upload response"