# FROM jupyter/tensorflow-notebook:latest
FROM jupyter/tensorflow-notebook:d990a62010ae

RUN pip install plotly==4.14.3
RUN pip install nltk==3.5
RUN pip install torch==1.8.0
RUN pip install torchvision==0.9.0
RUN pip install pytorch-nlp==0.5.0
RUN pip install gensim==3.8.3
RUN pip install transformers==4.3.3
RUN pip install nlp==0.4.0
  

RUN python -m nltk.downloader stopwords

RUN pip install pandas-datareader
RUN pip install -U sec-edgar-downloader

# docker build -t jupyter/stanford-final .
# docker run --rm -p 8888:8888 -v "$PWD":/home/jovyan/work jupyter/stanford-final