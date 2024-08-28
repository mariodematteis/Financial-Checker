FROM continuumio/miniconda3:latest

ARG ENV_FILE="environment.yml"
ARG ENV_NAME="FinancialChecker"

COPY .. /app
WORKDIR /app
RUN conda env create -f environment.yml

EXPOSE 8501

CMD ["conda", "run", "-n", "FinancialChecker", "streamlit", "run", "./src/financialchecker/app/main.py"]
