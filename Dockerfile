FROM apache/airflow:2.4.1
USER airflow

#ARG KAGGLE_USERNAME
#ARG KAGGLE_KEY

#RUN mkdir -p $HOME/.kaggle
COPY requirements.txt /requirements.txt
#COPY kaggle.json $HOME/.kaggle/kaggle.json

RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt