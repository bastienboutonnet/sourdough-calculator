FROM ubuntu

EXPOSE 8501

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    python3.10 \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip
RUN pip3 install .

ENTRYPOINT ["streamlit", "run", "/app/src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
