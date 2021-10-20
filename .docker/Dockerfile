FROM continuumio/miniconda3:latest
MAINTAINER 4A7G0029@stust.edu.tw
ARG ENV_YAML

WORKDIR Graduation-Project
COPY ${ENV_YAML} ./

RUN apt update
RUN apt upgrade -y
RUN apt install libgl1-mesa-glx -y

RUN conda update conda -y
RUN conda env update --name base --file ${ENV_YAML} --prune
