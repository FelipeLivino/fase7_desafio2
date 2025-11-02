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
    Função principal para rodar a detecção de objetos em uma imagem estática.
    """
    # --- Configuration for Static Image ---
    IMAGE_PATH = 'treinamento/images/teste/405.jpeg'
    OUTPUT_IMAGE_PATH = 'detection_result.jpg'

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

    print(f"Carregando a imagem de: {IMAGE_PATH}")
    # Carrega a imagem estática
    frame = cv2.imread(IMAGE_PATH)

    if frame is None:
        print(f"Erro ao carregar a imagem. Verifique o caminho: {IMAGE_PATH}")
        return

    print("Iniciando a detecção na imagem...")
    # Executa a inferência no frame
    results = model(frame)

    # Renderiza os resultados no frame
    rendered_frame = np.squeeze(results.render())

    # Salva a imagem com as detecções
    cv2.imwrite(OUTPUT_IMAGE_PATH, rendered_frame)
    print(f"Detecção concluída. Resultado salvo em: {OUTPUT_IMAGE_PATH}")

    # Opcional: exibir a imagem se estiver em um ambiente com GUI
    # cv2.imshow('YOLOv5 Detection Result', rendered_frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()