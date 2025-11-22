import cv2
import torch
import numpy as np
from urllib.request import urlopen
import os

# --- Path Configuration ---
# Build paths relative to the script's location for robustness
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, 'best.pt') 
INPUT_FOLDER = os.path.join(SCRIPT_DIR, 'input_images')
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, 'output_detections')

# --- Other Configurations ---
# URL do stream de vídeo da Raspberry Pi
STREAM_URL = 'http://192.168.0.142:5000/video_feed' 

# --- Main Application ---

def main():
    """
    Função principal para rodar a detecção de objetos em imagens de uma pasta.
    """
    # Cria a pasta de saída se não existir
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Define o dispositivo: usa a GPU (cuda) se estiver disponível, senão a CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando o dispositivo: {device}")
    
    if not torch.cuda.is_available():
        print("AVISO: CUDA não está disponível. Rodando na CPU.")

    print("Carregando modelo YOLOv5...")
    # Carrega o modelo do hub do PyTorch, usando o repositório oficial do YOLOv5.
    # Isso fará o download do modelo na primeira execução.
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, trust_repo=True)
    model.to(device)

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