import azure.functions as func
from azure.identity import DefaultAzureCredential
import logging

from http_function import http_func
#from blob_trigger import blob_func

app = func.FunctionApp()

app.register_functions(http_func)
#app.register_functions(blob_func)
    

