# Prisma

Node.js and Typescript ORM

## Prereqs

1. install Node

    ```zsh

    sudo apt-get update
    sudo apt-get install nodejs
    node --version
    npm -v

    ```

2. Start MongoDB

## Starting Mongo

```bash
export NAME="prisma_mongo"          # container name
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
export DB_NAME="my_prisma"
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

Considder the follwoing json and how you might divide it up into pieces for your database

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