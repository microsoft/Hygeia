import azure.functions as func
from azure.identity import DefaultAzureCredential
import logging

from http_blueprint import bp

app = func.FunctionApp()

app.register_functions(bp)
    

