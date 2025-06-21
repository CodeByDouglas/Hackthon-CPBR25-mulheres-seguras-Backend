import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

# Instancia o cliente Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def enviar_sms(to_number: str, body: str) -> str:
    """
    Envia um SMS usando Twilio e retorna o SID da mensagem.
    :param to_number: Número de destino (ex: +5511999999999)
    :param body: Texto da mensagem
    :return: SID da mensagem enviada
    :raises Exception: Em caso de erro no envio
    """
    try:
        # Envia a mensagem SMS
        message = client.messages.create(
            to=to_number, from_=TWILIO_FROM_NUMBER, body=body
        )
        return message.sid
    except TwilioRestException as e:
        # Loga o erro e relança uma exceção legível
        print(f"Erro ao enviar SMS: {e}")
        raise Exception(f"Falha ao enviar SMS: {e.msg}")
