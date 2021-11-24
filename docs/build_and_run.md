Quick and dirty - will port to python later.

This project will manage the lifecycle of a static website hosted in an azure storacge bucket with the long-term goal of using minio and kubernetes to self-host.

For full documentation visit [mkdocs.org](https://www.mkdocs.org).


## 1. Creating the Azure Resources

I have anoother project that will do this in terraform but I dont have the time to hook it up right now since its still aplpha.


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
cloudydev.net  AzureCloud   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      Enabled  True
    ```
```

## 5. Export variables and keep things DRY
    
```bash
export KIND=" "
export LOCATION=" "
export SUBSCRIPTION=" "
export RG_NAME=" "
export STORAGE_NAME=" "
export STORAGE_SKU=" "
export ERROR_DOC=" "
export INDEX_DOC=" "
export SITE_ROOT_FOLDER=" "
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
  --allow-blob-public-access=true \
  --sku="${STORAGE_SKU}" \
  --kind="${KIND}"

az storage account show \
  --name="${STORAGE_NAME}" \
  --resource-group="${RG_NAME}" \
  --query allowBlobPublicAccess \
  --output tsv

az storage account update \
  --name="${STORAGE_NAME}" \
  --resource-group="${RG_NAME}" \
  --allow-blob-public-access true

az storage container create \
  --name '$web' \
  --account-name="${STORAGE_NAME}" \
  --resource-group="${RG_NAME}" \
  --public-access off \
  --auth-mode login

az storage container show-permission \
  --name '$web' \
  --account-name="${STORAGE_NAME}"

az storage container set-permission \
  --name '$web' \
  --account-name="${STORAGE_NAME}" \
  --public-access=container
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

