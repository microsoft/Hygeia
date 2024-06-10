import io
import logging 
import azure.functions as func 
from plugins.kernel_memory_plugin import KernelMemoryPlugin
from semantic_kernel.kernel import Kernel
import azurefunctions.extensions.bindings.blob as blob
# from azure.identity import DefaultAzureCredential


blob_func = func.Blueprint() 

# credentials = DefaultAzureCredential()

# @blob_func.function_nam(name="BlobTrigger")
#@blob_func.blob_trigger(arg_name="blobFile", path="upload/{id}", connection="STORAGE_CONNECTION_STRING")
#async def blob_upload(blobFile: func.InputStream):
@blob_func.blob_trigger(
    arg_name="client", path="upload/{id}", connection="STORAGE_CONNECTION_STRING"
)
async def blob_upload(client: blob.BlobClient):
    blob_props = client.get_blob_properties()

    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Properties: {blob_props}\n"
    )
    
    kernel = Kernel()
    
    kmPlugin = kernel.add_plugin(KernelMemoryPlugin(), "KernelMemoryPlugin")

    stream = io.BytesIO()
    num_bytes = client.download_blob().readinto(stream)
    logging.info(f"Blob size in bytes: {num_bytes}")
    
    response = await kernel.invoke(kmPlugin["upload"], file=stream.getvalue(), file_name=blob_props["name"], document_id="")

    if response:    
        logging.info(f"Response: {response}")
    else:
        logging.info("Response: No response")
