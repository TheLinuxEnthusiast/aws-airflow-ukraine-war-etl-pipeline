#!/bin/bash

AIRFLOW_HOME_DIR="/opt/airflow"
KAGGLE_USER="piterfm"
KAGGLE_DATASET="2022-ukraine-russian-war"
FILE_NAME="${KAGGLE_DATASET}.zip"

#Check if Old file exists, if yes then remove
[ -f "${AIRFLOW_HOME_DIR}/dags/datasets/${FILE_NAME}" ] && rm -f ${AIRFLOW_HOME_DIR}/dags/datasets/${FILE_NAME}

# Extract Data from Kaggle
which kaggle
if [ "$?" = 0 ];
then
    kaggle datasets download ${KAGGLE_USER}/${KAGGLE_DATASET} -p ${AIRFLOW_HOME_DIR}/dags/datasets
fi

# Unzip file
#unzip -o ${AIRFLOW_HOME_DIR}/dags/datasets/${FILE_NAME} -d ${AIRFLOW_HOME_DIR}/dags/datasets
