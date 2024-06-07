import os
import logging 
import azure.functions as func 
from plugins.kernel_memory_plugin import KernelMemoryPlugin
from semantic_kernel.kernel import Kernel
# from azure.identity import DefaultAzureCredential

blob_func = func.Blueprint() 

# credentials = DefaultAzureCredential()

# @blob_func.function_nam(name="BlobTrigger")
@blob_func.blob_trigger(arg_name="blobFile", path="smemory/{id}", connection="STORAGE_CONNECTION_STRING")
async def blob_upload(blobFile: func.InputStream):
    logging.info(f"Python HTTP trigger function processed a request for {blobFile.name}.")
    
    kernel = Kernel()

    kmPlugin = kernel.add_plugin(KernelMemoryPlugin(), "KernelMemoryPlugin")

    response = await kernel.invoke(kmPlugin["upload"], file=blobFile.name)

    if response:    
        logging.info(f"Response: {response}")
    else:
        logging.info("Response: No response")

.







    # 1. Get the blob
    # 2. create instance of our custom kernelmemoryplugin <- PHIL TODO GET IT DONE
    # 3. call the kernelmemoryplugin to store the blob
    
    #kernel = Kernel()
    #kernelmemfunc = kernel.import_plugin(KernelMemroyPlugin)
    #kernel.invoke(kernelmemfunc, "store_blob", name)
