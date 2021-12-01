
# Just Docs

 [Just the docs](https://pmarsceill.github.io/just-the-docs/), a jekyll theme that generates documentation sites from markdown.

1. Install ruby and other deps.

    ```zsh
    # install ruby
    sudo apt-get install ruby-full

    # download the gems package manager
    wget https://github.com/rubygems/rubygems/archive/refs/tags/bundler-v2.2.28.zip

    # extract
    unzip bundler-v2.2.28.zip

    # navigate to the new directory
    cd rubygems-bundler-v2.2.28/

    # run the setup program
    sudo ruby setup.rb

    # install the just-the-docs software
    sudo gem install just-the-docs
    sudo gem install bundler
    ```

2. Create a gemfile

    ```rb
    # ./Gemfile
    source 'https://rubygems.org'
    gem 'just-the-docs'
    gem 'bundler'
    ```

3. Now add Just the Docs to your Jekyll site’s _config.yml

    ```yaml
    theme: "just-the-docs"
    #remote_theme: pmarsceill/just-the-docs
    color_scheme: dark
    aux_links:
      "Just the Docs on GitHub":
        - "//github.com/pmarsceill/just-the-docs"
    aux_links_new_tab: true
    ```

4. Serve the website

    ```zsh

    cd just_docs

    bundle exec jekyll serve

    ```

  - View at [http://127.0.0.1:4000](http://127.0.0.1:4000)
