# __Hazelcast IMDG__ 

[Hazelcast IMDG](https://docs.hazelcast.com/imdg/) is an __In Memory Data-Grid__, which holds all your data and can distribute it to other clients quickly without ever hitting a disk. It works well to move data and process data qucikly in an event-listener or observer pattern. Its also a good buffer between the database and the application.

Hazelcast stands out from other memory-caches like Redis is that it is multi-core and scales much more evenly as well as retains 
more open source offerings in its environment. It is also faster than some other memory caches due to its near-caching strategy.

!!! warning

    Hazelcast is __NOT__ a databse and shouldnt be your primary perisistancy solution.

___

## __Install__ 

- __Server__

    ```zsh
    # download keys and install via apt
    wget -qO - https://repository.hazelcast.com/api/gpg/key/public |     sudo apt-key add -
    echo "deb https://repository.hazelcast.com/debian stable main" |     sudo tee -a /etc/apt/sources.list
    sudo apt update && sudo apt install hazelcast

    ```

- __Client__

    Install pip package
    
    ```zsh
    pip install hazelcast-python-client
    ```

    Python Example:
    
    ```python    
    import hazelcast
    
    if __name__ == "__main__":

        # Start the client and connect to the cluster
        hz = hazelcast.HazelcastClient()
        
        # Create a Distributed Map in the cluster
        map = hz.get_map("my-distributed-map").blocking()
        
        # Standard Put and Get
        map.put("1", "John")
        map.put("2", "Mary")
        map.put("3", "Jane")
        
        # Shutdown the client
        hz.shutdown()
    ```

## Connecting 

__Start the Management Center__

```zsh
hz mc start
```

View on: http://localhost:8080

If using Docker for members, find out the Docker IP address ofcluster rather than the default of localhost.

__Discovering Members__

Kubernetes:

  - Uses the [Discovery Plugin](https://github.com  hazelcasthazelcast-kubernetes), follow the guide on the site

    ```zsh
    # add permissions for the default account in the default       namespace
    kubectl apply -f https://raw.githubusercontent  comhazelcast/      hazelcast-kubernetes/master/rbac.yaml
    
    ```

  - Create a service
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: MY-SERVICE-NAME
    spec:
      type: LoadBalancer
      selector:
        app: APP-NAME
      ports:
      - name: hazelcast
        port: 5701  
    ```
      
  - Configure hazelcast
  
    hazelcast.yaml:
    ```yaml
    hazelcast:
    network:
      join:
        multicast:
          enabled: false
        kubernetes:
          enabled: true
          namespace: MY-KUBERNETES-NAMESPACE
          service-name: MY-SERVICE-NAME  
    ```