# Base Python
FROM python:3.10

# Diretório da aplicação
WORKDIR /app

# Copia requirements
COPY requirements.txt /app/

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . /app

# Expõe a porta do Streamlit
EXPOSE 8507

# Executa o Streamlit
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8507"]
