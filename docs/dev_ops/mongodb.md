# MongoDB

> mongoDB is a NoSQL database w/ live resizing of shards that can be run in a container

Links:

- [mongo in docker](https://hub.docker.com/_/mongo)
- [tags](https://github.com/docker-library/docs/blob/master/mongo/README.md#supported-tags-and-respective-dockerfile-links)
- [config file options](https://docs.mongodb.com/manual/reference/configuration-options/)
- [Docker for mac bug](https://github.com/docker/for-mac/issues/3677). Docker Desktop on mac OS has a HUGE performance penalty for mounting binds, this causes the scripts to timeout on mac.

## Containerized
- Starting Mongo

    ```bash
    export NAME="my_mongo"          # container name
    export VERSION="mongo:latest"   # mongo version
    export MEM_LIMIT_GB=1.5         # memory usage limit
    export PORT="27017"             # Port to listen on

    #persistant volume root dir
    export PV="tmp"
    export DB_VOLUME="${PV}/db"     # DB volume
    export AUTH_VOLUME="${PV}/auth" # auth volume
    export PWD_FILE="DB_PWD"        # auth file
    export DB_USN="admin"           # username
    export DB_PWD="123password"     # password, will be removed when Key Vault connected
    export NETWORK_TYPE="bridge"    # bridge/host/macvlan/none
    export DB_NAME="my_app"
    export COLLECTION="environments"

    # initialize dirs we will need (tests only, wont be here in prod)
    mkdir ./$PV
    mkdir ./$AUTH_VOLUME
    mkdir ./$DB_VOLUME
    echo $DB_PWD > $AUTH_VOLUME/$PWD_FILE

    # Pull Mongo:
    docker pull mongo

    # Start MongoDB:
    docker run -d --network $NETWORK_TYPE \
        --name $NAME \
        --mount type=bind,source="$(pwd)"/$AUTH_VOLUME,target=/auth \
        --mount type=bind,source="$(pwd)"/$DB_VOLUME,target=/var \
        -e "MONGO_INITDB_ROOT_USERNAME=${DB_USN}" \
        -e "MONGO_INITDB_ROOT_PASSWORD_FILE=/auth/${PWD_FILE}" \
        -e "MONGO_INITDB_DATABASE=admin" \
        $VERSION \
        --wiredTigerCacheSizeGB $MEM_LIMIT_GB

    # start a jump sessions to execute commands in the shell
    docker exec -it $NAME sh -c "mongosh -u '${DB_USN}' -p '${DB_PWD}'"
    ```

## Setup a new DB

- Refer to [mongosh manual](https://docs.mongodb.com/mongodb-shell/run-commands/) for more in-depth information.

- Considder the follwoing json and how you might divide it up into pieces for your database

    ```JSON
    {
      "app": "my_app",
      "env_name": "production",
      "client": "Brand",
      "int_array": [
          1,
          22,
          100
      ],
      "dict": {
         "debug":"false"
       }
    }
    ```

1. create a new database for the data type

    ```zsh
    # switch to a new DB
    use my_app

    ```

2. insert a new collection.document into the database

    ```zsh
    db.environments.insertOne(
        {
          "env_name": "production",
          "client": "Brand",
          "int_array": [ 1, 22, 100 ],
          "dict": { "debug" : "false" },
          "release": "1.1"
        }
    )
    ```

3.  insert an array of documents into a collection

    ```zsh
    db.environments.insertMany([
        {
          "env_name": "production",
          "client": "Brand",
          "int_array": [ 1, 22, 70 ],
          "dict": { "debug" : "false" },
          "release": "1.1"
        },
        {
          "env_name": "production",
          "client": "Brand",
          "int_array": [ 1, 2, 1 ],
          "dict": { "debug" : "false" },
          "release": "1.2"
        },
        {
          "env_name": "test",
          "client": "Brand",
          "int_array": [ 1, 22, 100 ],
          "dict": { "debug" : "true" },
          "release": "1.3"
        },
        {
          "env_name": "dev",
          "client": "Brand",
          "int_array": [ 1, 22, 100 ],
          "dict": { "debug" : "true" },
          "release": "1.3"
        },
        {
          "env_name": "dev",
          "client": "Brand",
          "int_array": [ 1, 2, 1 ],
          "dict": { "debug" : "true" },
          "release": "1.2"
        }
    ])
    ```

4. return all in collection

    ```zsh
     db.getCollection("environments").find({});

    ```

5. find in collection

    ```zsh
     db.getCollection("environments").find({ "env_name": "test" })
     db.getCollection("environments").find({ "client": "Brand" })
     db.getCollection("environments").find({ "release": "1.3" })
    ```

## Serialize


1. mongodump
    
    ```zsh
    mongodump --collection='${COLLECTION}' \
        --db='${DB_NAME}' \
        --out=/var/'${COLLECTION}' \
        -u '${DB_USN}' \
        -p '${DB_PWD}' \
        --authenticationDatabase="admin"

    sudo docker exec $NAME sh -c \
        'exec mongodump --collection='${COLLECTION}' \
            --db='${DB_NAME}' \
            --out=/var/'${COLLECTION}' \
            --username='${DB_USN}' \
            --password='${DB_PWD}' \
            --authenticationDatabase="admin"'
    ```

2. mongoexport

    ```zsh
    mongoexport --collection='${COLLECTION}' \
        --db='${DB_NAME}' \
        --out=/var/'${COLLECTION}' \
        -u '${DB_USN}' \
        -p '${DB_PWD}' \
        --authenticationDatabase="admin"

    sudo docker exec $NAME sh -c \
        'exec mongoexport --collection='${COLLECTION}' \
            --db='${DB_NAME}' \
            --jsonFormat=canonical \
            --out=/var/'${COLLECTION}'.json \
            --username='${DB_USN}' \
            --password='${DB_PWD}' \
            --authenticationDatabase="admin"'
    ```

3. mongorestore

    ```zsh
    mongorestore /var/'${COLLECTION}' \
        --username='${DB_USN}' \
        --password='${DB_PWD}' \
        --authenticationDatabase="admin"

    sudo docker exec $NAME sh -c \
        'exec mongorestore /var/archive \
            --username='${DB_USN}' \
            --password='${DB_PWD}' \
            --authenticationDatabase="admin"'
    ```

4. bsondump

    ```zsh
    sudo docker exec $NAME sh -c \
        'exec bsondump \
            --outFile="/var/archive/'${DB_NAME}'/'${COLLECTION}'.json" \
            "/var/archive/'${DB_NAME}'/'${COLLECTION}'.bson"'

    ```
