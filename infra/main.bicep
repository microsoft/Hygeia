// Main bicep template
targetScope = 'resourceGroup'

param openAIEndpoint string
param managedIdentityClientId string
param location string = resourceGroup().location
param prefix string = 'hygeia${uniqueString(resourceGroup().id)}'
param tags object = {}

module apim 'modules/gateway/apim.bicep' = {
  name: 'apim'
  params: {
    applicationInsightsName: 'appInsightsName'
    name: '{prefix}-apim'
    location: location
    sku: 'Consumption'
  }
}

module aoaiApi 'modules/gateway/openai-apim-api.bicep' = {
  name: 'aoaiApi'
  params: {
    apiManagementServiceName: apim.outputs.apimServiceName
    managedIdentityClientId: managedIdentityClientId
    openAIEndpoint: openAIEndpoint
  }
}
