import cv2
import torch
import numpy as np
import os
from alert_service import AlertService

# --- AWS Configuration ---
# O ARN do tópico SNS para o qual os alertas serão enviados.
# Substitua pelo ARN do seu tópico SNS ou configure como variável de ambiente.
# Você pode encontrar o ARN no console da AWS em Simple Notification Service > Topics
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:MyAlertingTopic")


# --- Path Configuration ---
# Build paths relative to the script's location for robustness
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, 'best.pt') 
INPUT_FOLDER = os.path.join(SCRIPT_DIR, 'input_images')
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, 'output_detections')


def process_detection_results(results, filename, alert_service):
    """
    Processa os resultados da detecção, extrai informações sobre os animais
    e envia alertas se animais doentes forem detectados.
    """
    labels = results.pandas().xyxy[0]['name'].tolist()
    sick_animals = [label for label in labels if "doente" in label.lower()]

    if sick_animals:
        print(f"Atenção: Animais doentes detectados na imagem {filename}: {', '.join(sick_animals)}")
        
        # Prepara a mensagem de alerta
        animal_id = filename.split('.')[0]
        status = "Doente"
        action = "Veterinário acionado para avaliação e tratamento."
        message = f"Alerta de Saúde Animal:\n\n" \
                  f"Animal ID (imagem): {animal_id}\n" \
                  f"Status Detectado: {status} ({', '.join(sick_animals)})\n" \
                  f"Ação Sugerida: {action}"
        subject = f"Alerta de Saúde Animal: {animal_id}"

        # Envia o alerta
        alert_service.send_alert(SNS_TOPIC_ARN, message, subject)
    else:
        print(f"Nenhum animal doente detectado na imagem {filename}.")


def main():
    """
    Função principal para rodar a detecção de objetos em imagens de uma pasta.
    """
    # Cria a pasta de saída se não existir
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Inicializa o serviço de alerta
    alert_service = AlertService(region_name='us-east-1')

    # Define o dispositivo: usa a GPU (cuda) se estiver disponível, senão a CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando o dispositivo: {device}")
    
    if not torch.cuda.is_available():
        print("AVISO: CUDA não está disponível. Rodando na CPU.")

    print("Carregando modelo YOLOv5...")
    # Carrega o modelo do hub do PyTorch, usando o repositório oficial do YOLOv5.
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

            # Processa os resultados da detecção e envia alertas se necessário
            process_detection_results(results, filename, alert_service)

            # Renderiza os resultados no frame
            rendered_frame = np.squeeze(results.render())

            # Salva a imagem com as detecções na pasta de saída
            output_image_path = os.path.join(OUTPUT_FOLDER, f"detected_{filename}")
            cv2.imwrite(output_image_path, rendered_frame)
            print(f"Detecção concluída. Resultado salvo em: {output_image_path}")

    print("Processamento de todas as imagens concluído.")

if __name__ == '__main__':
    main()