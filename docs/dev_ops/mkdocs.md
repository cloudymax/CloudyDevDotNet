# Creating documentation websites with mkDocs


1. Install and create a project:

    ```zsh
    # Install:
      pip install mkdocs
      pip install mkdocs-material


    # Create a new project
     mkdocs new my-project

    # navigate to the project directory
    cd my-project

    # add the documentation builds to gitignore
    echo "app/site/" >> .gitignore
    ```

2. Add the material theme to `mkdocs.tml`

    ```yaml
    site_name: My Docs
    theme:
        name: material
    ```

3. Serve the page to localhost:

    ```zsh
    mkdocs serve
    ```

    View the site at:

    - [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


4. Build and deploy the site:

    ```zsh

    cd mkdocs

    # first time
    bash -x bad-deploy.sh first_publish

    # to update
    bash -x bad-deploy.sh update_site
    ```
