import streamlit as st
import os
from PIL import Image
import time

st.set_page_config(page_title="Resultados da Detecção", layout="wide")

st.title("Comparação de Imagens: Antes e Depois da Detecção")

# --- Configuração dos Caminhos ---
INPUT_FOLDER = 'input_images'
OUTPUT_FOLDER = 'output_detections'

# Espera até que a pasta de saída seja criada pelo script de detecção
# Isso é útil para garantir que o processamento tenha começado
wait_message = st.empty()
waited = 0
while not os.path.exists(OUTPUT_FOLDER) and waited < 30: # Espera no máximo 30 segundos
    wait_message.info(f"Aguardando a pasta de resultados '{OUTPUT_FOLDER}' ser criada pelo processamento inicial...")
    time.sleep(1)
    waited += 1

if not os.path.exists(OUTPUT_FOLDER):
    st.error(f"A pasta de saída '{OUTPUT_FOLDER}' não foi encontrada após {waited} segundos. O script de detecção pode ter falhado.")
else:
    wait_message.success("Pasta de resultados encontrada! Exibindo imagens.")

    # Lista as imagens de entrada
    try:
        input_images = sorted([f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

        if not input_images:
            st.warning(f"Nenhuma imagem encontrada na pasta de entrada '{INPUT_FOLDER}'.")

        for img_name in input_images:
            input_path = os.path.join(INPUT_FOLDER, img_name)
            output_name = f"detected_{img_name}"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            st.markdown(f"---")
            st.subheader(f"Processando: `{img_name}`")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("##### Antes")
                try:
                    image_before = Image.open(input_path)
                    st.image(image_before, use_column_width=True)
                except Exception as e:
                    st.error(f"Não foi possível carregar a imagem de entrada: {e}")

            with col2:
                st.markdown("##### Depois")
                if os.path.exists(output_path):
                    try:
                        image_after = Image.open(output_path)
                        st.image(image_after, use_column_width=True)
                    except Exception as e:
                        st.error(f"Não foi possível carregar a imagem processada: {e}")
                else:
                    st.warning("Imagem processada ainda não disponível. Atualize a página em instantes.")

    except FileNotFoundError:
        st.error(f"A pasta de entrada '{INPUT_FOLDER}' não foi encontrada.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao listar as imagens: {e}")
