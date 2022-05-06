#!/bin/bash
#This all needs to go in CI whenever I get some time
set -e
set -u
set -o pipefail

pip install mkdocs
pip install mkdocs-material
brew update && brew install azure-cli

export KIND="StorageV2"
export LOCATION="westeurope"
export SUBSCRIPTION="cloudydev.net"
export RG_NAME="cloudydev-docs"
export STORAGE_NAME="cloudydevdata"
# Standard Read-Access Geo Replicated Storage
export STORAGE_SKU="Standard_RAGRS"
export ERROR_DOC="index.html"
export INDEX_DOC="index.html"
export SITE_ROOT_FOLDER="site"

# set subscription
az account set \
        --subscription="${SUBSCRIPTION}"


first_run(){

az account set --subscription="${SUBSCRIPTION}"

az group create \
  -l="${LOCATION}" \
  -n="${RG_NAME}"

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

az storage blob service-properties update \
  --account-name="${STORAGE_NAME}" \
  --static-website \
  --404-document="${ERROR_DOC}" \
  --index-document="${INDEX_DOC}" \
  --auth-mode login

az storage blob upload-batch \
    -s "${SITE_ROOT_FOLDER}" \
    -d '$web' \
    --account-name="${STORAGE_NAME}"

az storage account show \
  -n "${STORAGE_NAME}" \
  -g "${RG_NAME}" \
  --query "primaryEndpoints.web" \
  --output tsv

}

build_and_deploy(){

# remove old files
rm -rf site

#build site
mkdocs build

# upload files
az storage blob upload-batch \
  -s "${SITE_ROOT_FOLDER}" \
  -d '$web' \
  --account-name="${STORAGE_NAME}" \
  --overwrite

# get the url
az storage account show \
  -n "${STORAGE_NAME}" \
  -g "${RG_NAME}" \
  --query "primaryEndpoints.web" \
  --output tsv

}

"$@"