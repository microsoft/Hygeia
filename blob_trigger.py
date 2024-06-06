import logging 

import azure.functions as func 

blob_func = func.Blueprint() 

@blob_func.blob_trigger("myblob/{name}", connection="AzureWebJobsStorage")
def blob_upload(name: str):
    logging.info('Python HTTP trigger function processed a request.') 

    # 1. Get the blob
    # 2. create instance of our custom kernelmemoryplugin <- PHIL TODO GET IT DONE
    # 3. call the kernelmemoryplugin to store the blob
    
    #kernel = Kernel()
    #kernelmemfunc = kernel.import_plugin(KernelMemroyPlugin)
    #kernel.invoke(kernelmemfunc, "store_blob", name)
    
    # remove all this pasted code below
    name = req.params.get('name') 
    if not name: 
        try: 
            req_body = req.get_json() 
        except ValueError: 
            pass 
        else: 
            name = req_body.get('name') 

    if name: 
        return func.HttpResponse( 
            f"Hello, {name}. This HTTP-triggered function " 
            f"executed successfully.") 
    else: 
        return func.HttpResponse( 
            "This HTTP-triggered function executed successfully. " 
            "Pass a name in the query string or in the request body for a" 
            " personalized response.", 
            status_code=200 
        )