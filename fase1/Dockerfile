# Use imagem oficial do Python
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivo de requirements primeiro (para cache de layers)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app_streamlit.py .

# Criar diretório para dados (storage.json)
RUN mkdir -p /app/data

# Instalar R e dependências necessárias
RUN apt-get update && apt-get install -y r-base r-base-dev && rm -rf /var/lib/apt/lists/*

# Criar diretório para scripts R (caso existam)
RUN mkdir -p /app/projeto_r/services

# Expor porta do Streamlit
EXPOSE 8501

# Configurar Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_ENABLEXSRFPROTECTION=false

# Comando para executar a aplicação
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501"]
