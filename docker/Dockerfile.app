FROM continuumio/miniconda3:latest

ARG ENV_FILE="environment.yml"
ARG ENV_NAME="FinancialChecker"

ADD ${ENV_FILE} /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

COPY .. /app
WORKDIR /app/src/FinancialChecker/app

CMD ["conda", "run", "-n", "FinancialChecker", "&&", "streamlit", "run", "main.py"]
