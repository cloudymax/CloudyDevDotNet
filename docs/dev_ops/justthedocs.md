---
layout: default
nav_exclude: true
---

# Just Docs

 [Just the docs](https://pmarsceill.github.io/just-the-docs/), a jekyl theme that generate documentation sites from markdown.

## Building locally

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

- Create a gemfile

```rb
# ./Gemfile
source 'https://rubygems.org'
gem 'just-the-docs'
gem 'bundler'
```

- Now add Just the Docs to your Jekyll site’s _config.yml

```yaml
theme: "just-the-docs"
#remote_theme: pmarsceill/just-the-docs
color_scheme: dark
aux_links:
  "Just the Docs on GitHub":
    - "//github.com/pmarsceill/just-the-docs"
aux_links_new_tab: true
```

- Serve the website

```zsh

cd just_docs

bundle exec jekyll serve

```

- View at [http://127.0.0.1:4000](http://127.0.0.1:4000)
