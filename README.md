# Generative Answers with RAG Endpoint

The purpose of this project is to provide templated example WebAPI endpoint that uses Azure OpenAI to answer user questions and provide instructions based on a set of internal documents with Retrievel Augmented Generation (RAG).

This template utilizes the following open source AI orchestration layers:
* Semantic Kernel SDK
    * [GitHub repo](https://github.com/microsoft/semantic-kernel)
    * [Microsoft Learn documentation](https://learn.microsoft.com/en-us/semantic-kernel/overview)
* [Kernel Memory Service](https://github.com/microsoft/kernel-memory)

## Architecture

![High Level Architecture](./docs/arch-high%20level%20arch%20v2.png)

## Components

This project repository includes the following components:

| Component | Description |
|---|---|
| [function_app.py](./function_app.py) | Defines the Azure Function and components (includes `http_function.py` and `blob_trigger.py`)|
| [http_function.py](./http_function.py) | A function defining an `/ask` API route, and orchestration logic behind it to perform a RAG pattern generative answer to a request |
| [blob_trigger.py](./blob_trigger.py) | A function triggered by blobs added to an `upload` container, which processes the blob into AI Search through the Kernel Memory pipeline |
| [Kernel Memory Plugin](./plugins/kernel_memory_plugin.py) | Plugin registered with the Semantic Kernel orchestration layer to interface with the Kernel Memory service `/ask`, `/search`, `/upload` and `/delete` endpoints. |
| [test web client app](./app) | A simple web front end for testing the API endpoint (not a chat interface) |
| [test.http](./test.http) | A test file for use with a `REST Client` extension |
| [deployment templates](./infra) | Bicep templates for deploying APIM configurations and policies for gateway to Azure OpenAI

## Pre-Requisites
The Kernel Memory service, not included in this project repository, is required. Follow deployment instructions from the below open source GitHub project.

> [Kernel Memory](https://github.com/microsoft/kernel-memory)<br>This repository presents best practices and a reference architecture for memory in specific AI and LLMs application scenarios

The Kernel Memory deployment includes fully configured:
* Kernel Memory Service (Azure Container App)
* Azure AI Search Service
* Azure OpenAI
* Azure Storage Account

## Run and Test Locally
This project requires the following to be installed on your development environment:
* [python version 3.11](https://www.python.org/downloads/release/python-3118/)
* [Azure Function Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python#install-the-azure-functions-core-tools)
* [Azurite Extension](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio%2Cblob-storage)

1. Clone and open this repo in your IDE (these instructions are for VSCode)
2. Create a `local.settings.json` file in the root directory with the values in the section below
3. Build dev environment, either a virtual environment or dev container:
    * Virtual Environment: 
        * Command Pallet > `Python: Create Environment`
        * select Python 3.11 interpreter
        * install `requirements.txt`
        * Command Pallet > `Azurite: Start`
    * Dev Container:
        * Command Pallet > `Dev Containers: Reopen in Container`
        * included dev container definition will be built and run
4. In the Run pane, start debugging with `Attach to Python Functions`

## Environment Settings
Use the following for a `local.settings.json` file, or to build Environment Variables for your deployed Azure Function:

```JSON

## Local Configuration
To run the function app locally, create a local.settings.json file with the following example and update with your own values:
``` json
{
    "IsEncrypted": false,
    "Host": {
      "CORS": "*"
    },
    "Values": {
      "AzureWebJobsStorage": "UseDevelopmentStorage=true",
      "FUNCTIONS_WORKER_RUNTIME": "python",
      "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
      "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": "",
      "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME": "",
      "AZURE_OPENAI_ENDPOINT": "",
      "KERNEL_MEMORY_SERVICE_ENDPOINT": "",
      "KERNEL_MEMORY_SERVICE_INDEX": "default",
      "STORAGE_CONNECTION_STRING": "",
      "AZUREAD_TENANT_ID": "",
      "AZUREAI_SEARCH_ADMIN_KEY": "",
      "AZUREAI_SEARCH_ENDPOINT": ""
    }
  }
```
| Setting | Description |
|---|---|
| AZURE_OPENAI_CHAT_DEPLOYMENT_NAME | The name of your Azure OpenAI chat model deployment |
| AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME | The name of your Azure OpenAI embeddings model deployment |
| AZURE_OPENAI_ENDPOINT | Endpoint URL of your Azure OpenAI resource, or your APIM gateway for Azure OpenAI |
| KERNEL_MEMORY_SERVICE_ENDPOINT | Endpoint URL of the Kernel Memory service container app |
| KERNEL_MEMORY_SERVICE_INDEX | The name of the index used for upload and search of documents. |
| STORAGE_CONNECTION_STRING | For the storage account used for uploading documents via the `blob_trigger` function. We recommend using the storage account deployed with the Kernel Memory service |
| AZUREAI_SEARCH_ADMIN_KEY | Admin Key of the Search Service deployed with the Kernel Memory service, used for Chat History |
| AZUREAI_SEARCH_ENDPOINT | Endpoing URL of the Search Service deployed with the Kernel Memory service, used for the Chat History |

## Deploy to Azure

### API Management Gateway
Bicep templates are provided to deploy and configure API Management as a gateway to manage scaling and resiliency of calls into your Azure OpenAI model deployments. See [APIM Infra Instructions](./infra/README.md) for deploying APIM to your Azure subscription.

### Function Deployment
To deploy the code to an Function App in your Azure subscription from VSCode:

1. Install the [Azure Resources](https://github.com/microsoft/vscode-azureresourcegroups) and [Azure Functions](https://github.com/microsoft/vscode-azurefunctions) VSCode extensions if not already.
2. In the `Azure ` panel of VSCode, sign into your Azure subscription
3. In the `WORKSPACE` tree, click the Azure Function icon at the top and select `Deploy to Azure` 
4. In the command pallet workflow, select an existing function or create new, using `Python 3.11`
5. Once deployment is complete, in the `Resources` tree, browse into your subscription and the `Function App` node to find your new function. 
6. Expand the function, right-click on `Application Settings`, and select `Upload Local Settings`
  > NOTE: Ensure your `local.settings.json` file is properly created and configured as defined above first

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
