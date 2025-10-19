import logging
from flask import current_app
from twilio.rest import Client
import pywhatkit
import datetime

logger = logging.getLogger(__name__)

def enviar_twilio(cliente, to_number=None):
    sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    token = current_app.config.get('TWILIO_AUTH_TOKEN')
    from_number = current_app.config.get('TWILIO_FROM_NUMBER')
    to = to_number or current_app.config.get('NOTIFY_NUMBER')
    if not (sid and token and from_number and to):
        logger.error("Twilio não configurado, pulando.")
        return {"erro": "Twilio não configurado"}

    client = Client(sid, token)
    body = f"Consulta FACTA\nCliente: {cliente['nome']}\nCPF: {cliente['cpf']}\nMargem: {cliente['margem']}\nConta: {cliente['conta']}\nData: {cliente['data']}"
    try:
        msg = client.messages.create(body=body, from_=from_number, to=to)
        logger.info("Twilio enviado SID=%s", msg.sid)
        return {"status": "ok", "sid": msg.sid}
    except Exception as e:
        logger.exception("Erro ao enviar via Twilio")
        return {"erro": str(e)}

def enviar_pywhatkit(cliente, to_number=None):
    to = to_number or current_app.config.get('NOTIFY_NUMBER')
    if not to:
        logger.error("Numero de notificação ausente.")
        return {"erro": "numero ausente"}

    hora = datetime.datetime.now()
    send_hour = hora.hour
    send_minute = (hora.minute + 1) % 60
    text = f"Consulta FACTA\nCliente: {cliente['nome']}\nCPF: {cliente['cpf']}\nMargem: {cliente['margem']}\nConta: {cliente['conta']}\nData: {cliente['data']}"
    try:
        pywhatkit.sendwhatmsg(to, text, send_hour, send_minute)
        logger.info("pywhatkit agendado para %s:%s", send_hour, send_minute)
        return {"status": "ok"}
    except Exception as e:
        logger.exception("Erro pywhatkit")
        return {"erro": str(e)}
