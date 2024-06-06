import azure.functions as func
from azure.identity import DefaultAzureCredential
import logging
import os
import openai
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.services.azure_text_embedding import AzureTextEmbedding
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.kernel import Kernel
from http_blueprint import bp

app = func.FunctionApp()

app.register_functions(bp)
    

