FROM python:alpine

# install pip
RUN apk add py3-pip

RUN pip install mkdocs
RUN pip install mkdocs-material

# set the source
ADD ./docs /home/docs
ADD mkdocs.yml /home/mkdocs.yml
WORKDIR /home

# build the site
RUN mkdocs build

ENTRYPOINT [ "/bin/sh" ]


# --mount type=bind,source="$(pwd)"/target,target=/app \
# 
#