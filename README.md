# Static website hosting on Azure Blob Storage for ~$0.05 /month

## 1. Install the Azure CLI

```zsh
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## 2. Log In

```zsh
az login
```

## 3. List Subscriptions

```zsh
❯ az account list -o table                     
Name           CloudName    SubscriptionId                            State    IsDefault
-------------  -----------  ------------------------------------      -------  -----------
cloudydev.net  AzureCloud   d520e0d1-8ce2-4bf3-bb06-443ee372cfec      Enabled  True
    ```
```

## 4. Export variables and keep things DRY
    
```bash
export KIND="StorageV2"
export LOCATION="westeurope"
export SUBSCRIPTION="cloudydev.net"
export RG_NAME="cloudydev-docs"
export STORAGE_NAME="cloudydevdata"
export STORAGE_SKU="Standard_RAGRS"
export ERROR_DOC="index.html"
export INDEX_DOC="index.html"
export SITE_ROOT_FOLDER="site"
```

## 5. Set subscription

```zsh
az account set --subscription="${SUBSCRIPTION}"
```

## 6. Create a resource group

```zsh
az group create \
  -l="${LOCATION}" \
  -n="${RG_NAME}"
```

## 7. Create storage account

- [Reference](https://docs.microsoft.com/en-us/rest/api/storagerp/srp_sku_types)

```zsh
  az storage account create \
    --name="${STORAGE_NAME}" \
    --resource-group="${RG_NAME}" \
    --location="${LOCATION}" \
    --sku="${STORAGE_SKU}" \
    --kind="${KIND}"
```

## 8. Enable static website hosting
 
```zsh
  az storage blob service-properties update \
    --account-name="${STORAGE_NAME}" \
    --static-website \
    --404-document="${ERROR_DOC}" \
    --index-document="${INDEX_DOC}" \
    --auth-mode login
```

## 9. Upload Files
    
```zsh
 az storage blob upload-batch \
     -s "${SITE_ROOT_FOLDER}" \
     -d '$web' \
     --account-name="${STORAGE_NAME}"
```

## 10. Get the URL

```zsh
az storage account show \
  -n "${STORAGE_NAME}" \
  -g "${RG_NAME}" \
  --query "primaryEndpoints.web" \
  --output tsv
# https://cloudydevdata.z6.web.core.windows.net/  
```
