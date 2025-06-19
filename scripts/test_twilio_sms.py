from app.services.twilio_service import enviar_sms

if __name__ == "__main__":
    numero_destino = "+5562993977594"
    mensagem = "Teste de SMS via Twilio - Hackathon Mulheres Seguras"
    try:
        sid = enviar_sms(numero_destino, mensagem)
        print(f"Mensagem enviada com sucesso! SID: {sid}")
    except Exception as e:
        print(f"Erro ao enviar SMS: {e}") 