# GCP side car proxy

- Accessing SQL instances in GCP requires the use of a sidecar proxy

    ```dockerfile
    #Use the official image as a parent image.
    FROM google/cloud-sdk:latest
    
    #Set the working directory.
    WORKDIR /usr/src/automation
    
    #install dependencies
    RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
    RUN apt-get install wget ca-certificates
    RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
    RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
    
    RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
    RUN chmod +x cloud_sql_proxy
    
    
    RUN apt-get update && apt-get install -y \
        zip \
        unzip \
        git \
        postgresql postgresql-contrib

    #authenticate service account
    RUN gcloud auth activate-service-account "" --key-file="" --project=""
    
    
    RUN ./cloud_sql_proxy -instances=":device"=tcp:5432 -credential_file="" &
    ```