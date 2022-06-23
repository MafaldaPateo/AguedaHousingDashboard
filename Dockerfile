# FROM continuumio/miniconda3:4.12.0
# LABEL maintainer "Fillipe Feitosa <fillfeitosa@gmail.com>"

# RUN mkdir code
# WORKDIR /code

# COPY env.yml . 
# RUN export LC_ALL=C
# RUN conda config --append channels conda-forge
# RUN conda env create -f env.yml 
# RUN conda activate Tese_Mestrado_MPS
# COPY ./ ./

# EXPOSE 8050

# CMD ["python", "./main.py"]

FROM python:3.8
LABEL maintainer "Fillipe Feitosa <fillfeitosa@gmail.com>"

RUN mkdir code
WORKDIR /code


RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive \
  apt-get install --assume-yes --no-install-recommends \
  gdal-bin \
  libgdal-dev \
  python3-dev \
  build-essential 
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /
RUN export LC_ALL=C
RUN pip3 install -r /requirements.txt --upgrade
RUN pip3 install --upgrade dash dash-core-components dash-html-components dash-renderer
# RUN pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
COPY ./ ./

EXPOSE 8050

CMD ["python", "./main.py"]

