# Tanzu mkDocs

  > Moving from __Just The Docs__ to __mkDocs__ because of constraints on color/formatting, input options, and hosting images. Using MkDocs w/ a material theme. This builds a static site which we then serve with __flask__.

Install and create a project:

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

Add the material theme to `mkdocs.tml`

```yaml
site_name: My Docs
theme:
    name: material
```

Serve the page to localhost:

```zsh
mkdocs serve
```

View the site at:

- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

___

Build and deploy the site:

```zsh

cd tanzu-mkdocs

# first time
bash -x bad-deploy.sh first_publish

# to update
bash -x bad-deploy.sh update_site
```
