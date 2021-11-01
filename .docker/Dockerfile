#FROM continuumio/miniconda3:latest
FROM pytorch/conda-cuda
MAINTAINER 4A7G0029@stust.edu.tw
ARG ENV_YAML

# set bash as current shell
RUN chsh -s /bin/bash
SHELL ["/bin/bash", "-c"]

# Set Work Directory
WORKDIR Graduation-Project
COPY ${ENV_YAML} ./

# Update Ubuntu env
RUN apt update
RUN apt upgrade -y

# Install Other Package
RUN apt install libgl1-mesa-glx -y

# Update Anaconda
#RUN conda update conda -y
## Install Env
#RUN conda env update --name base --file ${ENV_YAML} --prune

############

##FROM continuumio/miniconda3:latest
#FROM nvidia/cuda:11.4.2-devel-ubuntu20.04
#MAINTAINER 4A7G0029@stust.edu.tw
#ARG ENV_YAML
#
## set bash as current shell
#RUN chsh -s /bin/bash
#SHELL ["/bin/bash", "-c"]
#
## Set Work Directory
#WORKDIR Graduation-Project
#COPY ${ENV_YAML} ./
#
## Update Ubuntu env
#RUN apt update
#RUN apt upgrade -y
#
## Install Other Package
#RUN apt install libgl1-mesa-glx -y
#RUN apt install wget -y
#
## Install Anaconda3
#RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/anaconda.sh && \
#        /bin/bash ~/anaconda.sh -b -p /opt/conda && \
#        rm ~/anaconda.sh && \
#        ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
#        echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
#        find /opt/conda/ -follow -type f -name '*.a' -delete && \
#        find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
#        /opt/conda/bin/conda clean -afy
#
## set path to conda
#ENV PATH /opt/conda/bin:$PATH
#
#CMD export PATH=$PATH:/opt/conda/bin; /bin/echo -e "ADDITIONAL_PATH is /opt/conda/bin\nPATH is $PATH"
## Update Anaconda
#RUN conda update conda -y
### Install Env
##RUN conda env update --name base --file ${ENV_YAML} --prune
#