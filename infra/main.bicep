// Main bicep template
targetScope = 'resourceGroup'

@description('Name of existing user assigned identity. Will default to SystemAssigned if empty.')
param managedIdentityPrincipalName string = ''
param location string = resourceGroup().location
param prefix string = 'hygeia${uniqueString(resourceGroup().id)}'
param aoaiPrimaryAccount string = 'km-openai-e8a8fe'
param aoaiSecondaryAccount string = 'km-openai-e8a8fe'
param tags object = {}

module apim 'modules/gateway/apim.bicep' = {
  name: 'apim'
  params: {
    tags: tags
    applicationInsightsName: 'appInsightsName'
    name: '${prefix}-apim'
    location: location
    sku: 'Consumption'
    aoaiPrimaryAccount: aoaiPrimaryAccount
    aoaiSecondaryAccount: aoaiSecondaryAccount
  }
}

module aoaiApi 'modules/gateway/openai-apim-api.bicep' = {
  name: 'aoaiApi'
  params: {
    apiManagementServiceName: apim.outputs.apimServiceName
    managedIdentityPrincipalName: managedIdentityPrincipalName
  }
}
