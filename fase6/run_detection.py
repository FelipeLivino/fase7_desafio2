import cv2
import torch
import numpy as np
from urllib.request import urlopen
import os

# --- Configuration ---
# URL do stream de vídeo da Raspberry Pi
# IMPORTANTE: Substitua pelo endereço IP real da sua Raspberry Pi
STREAM_URL = 'http://192.168.0.142:5000/video_feed' 

# Caminho para os pesos do modelo YOLOv5
MODEL_PATH = 'treinamento/yolov5s_60.pt'

# Caminho para o repositório local do YOLOv5
YOLO_REPO_PATH = 'treinamento/yolov5'

# --- Main Application ---

def main():
    """
    Função principal para rodar a detecção de objetos em imagens de uma pasta.
    """
    # --- Configuration for Static Image Folder ---
    INPUT_FOLDER = '/app/fase6/input_images'
    OUTPUT_FOLDER = '/app/fase6/output_detections'

    # Cria a pasta de saída se não existir
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Define o dispositivo: usa a GPU (cuda) se estiver disponível, senão a CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando o dispositivo: {device}")
    
    if not torch.cuda.is_available():
        print("AVISO: CUDA não está disponível. Rodando na CPU.")

    print("Carregando modelo YOLOv5...")
    # Carrega o modelo do repositório local
    try:
        model = torch.hub.load(YOLO_REPO_PATH, 'custom', path=MODEL_PATH, source='local')
        model.to(device)
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        print(f"Verifique se o YOLO_REPO_PATH está configurado corretamente para: {os.path.abspath(YOLO_REPO_PATH)}")
        return

    print(f"Processando imagens da pasta: {INPUT_FOLDER}")
    # Lista todos os arquivos na pasta de entrada
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(INPUT_FOLDER, filename)
            print(f"Carregando a imagem de: {image_path}")
            frame = cv2.imread(image_path)

            if frame is None:
                print(f"Erro ao carregar a imagem. Verifique o caminho: {image_path}")
                continue

            print(f"Iniciando a detecção na imagem: {filename}...")
            # Executa a inferência no frame
            results = model(frame)

            # Renderiza os resultados no frame
            rendered_frame = np.squeeze(results.render())

            # Salva a imagem com as detecções na pasta de saída
            output_image_path = os.path.join(OUTPUT_FOLDER, f"detected_{filename}")
            cv2.imwrite(output_image_path, rendered_frame)
            print(f"Detecção concluída. Resultado salvo em: {output_image_path}")

    print("Processamento de todas as imagens concluído.")

if __name__ == '__main__':
    main()