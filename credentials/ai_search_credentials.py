from azure.identity import DefaultAzureCredential
from azure.core.credentials import TokenCredential, AccessToken

class AISearchCredentials(TokenCredential):
    _tenant_id: str
    _default_credential: DefaultAzureCredential
    
    def __init__(self, tenant_id: str):
        self._tenant_id = tenant_id
        self._default_credential = DefaultAzureCredential()

    def get_token(self, *scopes, **kwargs) -> AccessToken:
        return self._default_credential.get_token(*scopes, **kwargs)