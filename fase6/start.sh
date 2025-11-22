#!/bin/sh

# Navega para o diretório do aplicativo para garantir que os caminhos relativos funcionem
cd /app

# Executa o script de detecção de objetos.
# As saídas serão salvas na pasta 'output_detections'.
echo "-------------------------------------------"
echo "Iniciando o processamento das imagens..."
echo "-------------------------------------------"
python run_detection.py

echo "-------------------------------------------"
echo "Processamento concluído."
echo "Iniciando a interface gráfica..."
echo "Acesse em seu navegador: http://localhost:8506"
echo "-------------------------------------------"

# Inicia a aplicação Streamlit para exibir os resultados.
# O servidor será acessível a partir do host na porta mapeada.
streamlit run app_streamlit.py --server.port=8501 --server.address=0.0.0.0
