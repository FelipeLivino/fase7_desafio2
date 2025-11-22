import cv2
import numpy as np
import os
import yolov5
from alert_service import AlertService
import pathlib
import sys

# --- Pathlib Workarounds for Cross-Platform Model Loading ---
# Fix for 'WindowsPath' not found on Linux
pathlib.WindowsPath = pathlib.PosixPath

# Fix for 'pathlib._local' not found (older python/pathlib versions)
if 'pathlib._local' not in sys.modules:
    sys.modules['pathlib._local'] = pathlib

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
    # sick_animals = [label for label in labels if "doente" in label.lower()]

    # if sick_animals:
        # print(f"Atenção: Animais doentes detectados na imagem {filename}: {', '.join(sick_animals)}")
        
        # Prepara a mensagem de alerta
    message = f"Envio de alerta:\n\n" 
    subject = f"Alerta de Animal: "

    # Envia o alerta
    alert_service.send_alert(SNS_TOPIC_ARN, message, subject)
    # else:
    #     print(f"Nenhum animal doente detectado na imagem {filename}.")


def main():
    """
    Função principal para rodar a detecção de objetos em imagens de uma pasta.
    """
    # Cria a pasta de saída se não existir
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Inicializa o serviço de alerta
    alert_service = AlertService(region_name='us-east-1')

    print("Carregando modelo YOLOv5...")
    # Carrega o modelo
    model = yolov5.load(MODEL_PATH)

    print(f"Processando imagens da pasta: {INPUT_FOLDER}")
    # Lista todos os arquivos na pasta de entrada
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            image_path = os.path.join(INPUT_FOLDER, filename)
            print(f"Carregando a imagem de: {image_path}")
            
            print(f"Iniciando a detecção na imagem: {filename}...")
            # Executa a inferência no frame
            results = model(image_path)

            # Processa os resultados da detecção e envia alertas se necessário
            process_detection_results(results, filename, alert_service)

            # Draw detections manually using PIL to avoid OpenCV readonly array issues
            # Load the original image
            from PIL import Image, ImageDraw, ImageFont
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # Get detection results as pandas dataframe
            detections = results.pandas().xyxy[0]
            
            # Draw each detection
            for _, detection in detections.iterrows():
                # Get bounding box coordinates
                x1, y1, x2, y2 = int(detection['xmin']), int(detection['ymin']), int(detection['xmax']), int(detection['ymax'])
                conf = detection['confidence']
                cls = detection['name']
                
                # Draw rectangle (box)
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                
                # Draw label
                label = f"{cls} {conf:.2f}"          
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
                except:
                    font = ImageFont.load_default()
                draw.text((x1, y1 - 20), label, fill="red", font=font)
            
            # Save the image with detections
            final_output = os.path.join(OUTPUT_FOLDER, f"detected_{filename}")
            img.save(final_output)
            print(f"Detecção concluída. Resultado salvo em: {final_output}")

    print("Processamento de todas as imagens concluído.")

if __name__ == '__main__':
    main()
