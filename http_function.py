import logging 

import os
import json
import openai
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.services.azure_text_embedding import AzureTextEmbedding
from semantic_kernel.contents import ChatHistory
from semantic_kernel.kernel import Kernel
from semantic_kernel.memory import SemanticTextMemory, VolatileMemoryStore
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from azure.identity import DefaultAzureCredential

import azure.functions as func 

from plugins.kernel_memory_plugin import KernelMemoryPlugin

http_func = func.Blueprint() 

@http_func.route(route='ask', auth_level='anonymous', methods=['POST'])
#async def http_ask(req: func.HttpRequest, session_id: str) -> func.HttpResponse:
async def http_ask(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
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
    # deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    # embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    # endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    plugins_directory = os.path.join(os.path.dirname(__file__), "plugins")
    
    kernel = Kernel()
    
    service_id = "chat-gpt"
    chat_service = AzureChatCompletion(
        service_id=service_id,
    )
    kernel.add_service(chat_service)
    # embedding_gen = AzureTextEmbedding(
    #     service_id="ada",
    #     deployment=embedding_deployment,
    #     endpoint=endpoint,
    #     ad_auth_provider=get_azure_openai_token,
    # )
    
    # memory = SemanticTextMemory(storage=VolatileMemoryStore(), embeddings_generator=embedding_gen)

    kmPlugin = kernel.add_plugin(KernelMemoryPlugin(), "KernelMemoryPlugin")
    chatPlugin = kernel.add_plugin(parent_directory=plugins_directory, plugin_name="prompts")    
    
    history = ChatHistory()
    # fetch short term memories for sessionId (chat history)
    # if session_id:
    #     result = memory.get(collection="chat", key=session_id)
    #     if result:
    #         history = json.loads(result.text)    
    
    # fetch memories related to user prompt (RAG docs)
    search_results = []
    search_response = await kernel.invoke(kmPlugin["search"], query=prompt)
    search_json = json.loads(search_response.value)
    for result in search_json["results"]:
        search_results.append(result)
    
    history.add_user_message(prompt)
    #json.dumps(search_results)
    resp = await kernel.invoke(chatPlugin["chat"], chat_history=history, input_text=search_results)
    
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
    
    kernel = Kernel()

    kmPlugin = kernel.add_plugin(KernelMemoryPlugin(), "KernelMemoryPlugin")
    
    resp = await kernel.invoke(kmPlugin["deleteDocuments"], document_id=document_id)    
    
    if resp:
        # return resp as json
        return func.HttpResponse(str(resp), mimetype="application/json")
    else:
        return func.HttpResponse("Response: No response", status_code=resp.status_code)


def get_azure_openai_token() -> str:
    creds = DefaultAzureCredential()
    return creds.get_token("https://cognitiveservices.azure.com", tenant_id=os.getenv("AZUREAD_TENANT_ID")).token@http_func.route(route='documents', auth_level='anonymous', methods=['DELETE'])