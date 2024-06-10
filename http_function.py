import logging 

import os
import json
import openai
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.kernel import Kernel
import azure.identity

import azure.functions as func 

from plugins.kernel_memory_plugin import KernelMemoryPlugin

http_func = func.Blueprint() 

@http_func.route(route='ask', auth_level='anonymous', methods=['POST'])
async def http_ask(req: func.HttpRequest) -> func.HttpResponse:

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
    #creds = DefaultAzureCredential()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    plugins_directory = os.path.join(os.path.dirname(__file__), "plugins")
    
    kernel = Kernel()

    kmPlugin = kernel.add_plugin(KernelMemoryPlugin(), "KernelMemoryPlugin")
    chatPlugin = kernel.add_plugin(parent_directory=plugins_directory, plugin_name="chat")
    
    resp = await kernel.invoke(kmPlugin["ask"], question=prompt)
    # resp = await kernel.invoke(kmPlugin["search"], query=prompt)
    
    if resp:
        # return resp as json
        return func.HttpResponse(str(resp), mimetype="application/json")
    else:
        return func.HttpResponse("Response: No response")


@http_func.route(route='documents', auth_level='anonymous', methods=['DELETE'])
async def http_deleteDocuments(req: func.HttpRequest) -> func.HttpResponse:
    
    url_params = req.route_params

    document_id = url_params.get('documentId')
    
    if not document_id:
        try:
            req_body = req.get_json()
        except ValueError:
            raise RuntimeError("documentId data must be set in url query.")
        else:
            document_id = req_body.get('documentId')
            if not document_id:
                raise RuntimeError("documentId data must be set in url query.")

    # Get managed identity token and env vars
    #creds = DefaultAzureCredential()
    # deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    # embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    # endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    kernel = Kernel()

    kmPlugin = kernel.add_plugin(KernelMemoryPlugin(), "KernelMemoryPlugin")
    
    resp = await kernel.invoke(kmPlugin["deleteDocuments"], document_id=document_id)    
    
    if resp:
        # return resp as json
        return func.HttpResponse(str(resp), mimetype="application/json")
    else:
        return func.HttpResponse("Response: No response", status_code=resp.status_code)
