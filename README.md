Quick and dirty - will port to python later.

This project will manage the lifecycle of a static website hosted in an azure storage bucket with the long-term goal of using minio and kubernetes to self-host.

## 1. Creating the Azure Resources

I have another project that will do this in terraform but I don't have the time to hook it up right now since its still alpha.


## 2. Install the Azure CLI

```zsh
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## 3. Log In

```zsh
az login
```

## 4. List Subscriptions

```zsh
❯ az account list -o table                     
Name           CloudName    SubscriptionId                            State    IsDefault
-------------  -----------  ------------------------------------      -------  -----------
cloudydev.net  AzureCloud   d520e0d1-8ce2-4bf3-bb06-443ee372cfec      Enabled  True
    ```
```

## 5. Export variables and keep things DRY
    
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

## 6. Set subscription

```zsh
az account set --subscription="${SUBSCRIPTION}"
```

## 7. Create a resource group

```zsh
az group create \
  -l="${LOCATION}" \
  -n="${RG_NAME}"
```

## 8. Create storage account

- [Reference](https://docs.microsoft.com/en-us/rest/api/storagerp/srp_sku_types)

```zsh
  az storage account create \
    --name="${STORAGE_NAME}" \
    --resource-group="${RG_NAME}" \
    --location="${LOCATION}" \
    --sku="${STORAGE_SKU}" \
    --kind="${KIND}"
```

## 9. Enable static website hosting
 
```zsh
  az storage blob service-properties update \
    --account-name="${STORAGE_NAME}" \
    --static-website \
    --404-document="${ERROR_DOC}" \
    --index-document="${INDEX_DOC}" \
    --auth-mode login
```

## 10. Upload Files
    
```zsh
 az storage blob upload-batch \
     -s "${SITE_ROOT_FOLDER}" \
     -d '$web' \
     --account-name="${STORAGE_NAME}"
```

## 11. Get the URL

```zsh
az storage account show \
  -n "${STORAGE_NAME}" \
  -g "${RG_NAME}" \
  --query "primaryEndpoints.web" \
  --output tsv
# https://cloudydevdata.z6.web.core.windows.net/  
```

