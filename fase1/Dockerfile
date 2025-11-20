# Use imagem oficial do Python
FROM python:3.9-slim

# Atualiza e instala dependências do R
RUN apt-get update && apt-get install -y --no-install-recommends \
    r-base \
    r-base-dev \
    build-essential \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    gnupg \
    ca-certificates \
    # Dependências de sistema adicionadas para plumber, s2, units, systemfonts e sodium
    libudunits2-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libsodium-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN R -e "install.packages(c('plumber', 'httr', 'jsonlite'), repos='https://cloud.r-project.org')"

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivo de requirements primeiro (para cache de layers)
COPY requirements.txt .

COPY projeto_r ./projeto_r

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app_streamlit.py .

# Criar diretório para dados (storage.json)
RUN mkdir -p /app/data

# Expor porta do Streamlit
EXPOSE 8501

# Configurar Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_ENABLEXSRFPROTECTION=false

# Comando para executar a aplicação
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501"]
