#!/bin/bash

AIRFLOW_HOME_DIR="/opt/airflow"
KAGGLE_USER="piterfm"
KAGGLE_DATASET="2022-ukraine-russian-war"

which kaggle
if [ "$?" = 0 ];
then
    kaggle datasets download ${KAGGLE_USER}/${KAGGLE_DATASET} -p ${AIRFLOW_HOME_DIR}/dags/datasets
fi

