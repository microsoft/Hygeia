import logging 

import os
import openai
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.kernel import Kernel
import azure.identity

import azure.functions as func 

from plugins.kernel_memory_plugin import KernelMemoryPlugin

bp = func.Blueprint() 

@bp.route(route='ask', auth_level='anonymous', methods=['POST'])
def http_ask(req: func.HttpRequest) -> func.HttpResponse:

    prompt = req.params.get('prompt') 
    if not prompt: 
        try: 
            req_body = req.get_json() 
        except ValueError: 
            raise RuntimeError("prompt data must be set in POST.") 
        else: 
            prompt = req_body.get('prompt') 
            if not prompt:
                raise RuntimeError("prompt data must be set in POST.")

    # Get managed identity token and env vars
    creds = DefaultAzureCredential()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    kernel = Kernel()

    kmPlugin = kernel.add_plugin(KernelMemoryPlugin(), "KernelMemoryPlugin")
    
    resp = kernel.invoke(kmPlugin["ask"], question="Where is the event?")
    
