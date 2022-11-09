FROM continuumio/miniconda

EXPOSE 8501

WORKDIR /app

COPY . .
RUN conda update conda -y
RUN conda install -c conda-forge streamlit
RUN pip3 install -U pip
RUN pip3 install .

ENTRYPOINT ["streamlit", "run", "/app/src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
