import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class AlertService:
    def __init__(self, region_name='us-east-1'):
        """
        Inicializa o serviço de alerta com a região da AWS.
        As credenciais da AWS (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        devem ser configuradas no ambiente.
        """
        self.region_name = region_name
        self.sns_client = boto3.client('sns', region_name=self.region_name)

    def send_alert(self, topic_arn, message, subject):
        """
        Envia um alerta para um tópico SNS.

        :param topic_arn: O ARN do tópico SNS.
        :param message: A mensagem a ser enviada.
        :param subject: O assunto do e-mail de notificação.
        :return: A resposta do SNS ou None em caso de erro.
        """
        try:
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject
            )
            print(f"Alerta enviado com sucesso para o tópico {topic_arn}. MessageId: {response['MessageId']}")
            return response
        except (NoCredentialsError, PartialCredentialsError):
            print("Erro: Credenciais da AWS não encontradas.")
            print("Por favor, configure as variáveis de ambiente AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY.")
            return None
        except Exception as e:
            print(f"Erro ao enviar o alerta: {e}")
            return None

# Exemplo de como usar a classe
if __name__ == '__main__':
    # Substitua pelo ARN do seu tópico SNS
    # Você pode encontrar o ARN no console da AWS em Simple Notification Service > Topics
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:MyAlertingTopic"
    
    alert_service = AlertService(region_name='us-east-1')

    # Exemplo de mensagem de alerta
    animal_id = "VACA-001"
    status = "Doente"
    action = "Veterinário acionado para avaliação."
    message = f"Alerta de Saúde Animal:\n\nAnimal: {animal_id}\nStatus: {status}\nAção Sugerida: {action}"
    subject = f"Alerta de Saúde: {animal_id} está {status}"

    alert_service.send_alert(SNS_TOPIC_ARN, message, subject)
