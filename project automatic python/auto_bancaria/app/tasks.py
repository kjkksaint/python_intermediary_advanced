import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from .api_facta import consultar_facta
from .processador import tratar_dados
from .notificacao import enviar_twilio, enviar_pywhatkit
from .banco import session
from .models import Consulta

logger = logging.getLogger(__name__)

def executar_ciclo(cpf):
    logger.info("Iniciando ciclo para CPF %s", cpf)
    api_data = consultar_facta(cpf)
    resultado = tratar_dados(api_data)
    if resultado.get('status') != 'ok':
        logger.warning("Ciclo terminou com erro: %s", resultado)
        return resultado

    cliente = resultado['cliente']
    # salvar no banco
    c = Consulta(cpf=cliente['cpf'], nome=cliente['nome'], margem=cliente['margem'],
                 conta=cliente['conta'], raw=cliente['raw'])
    session.add(c)
    session.commit()
    logger.info("Consulta salva ID=%s CPF=%s", c.id, cliente['cpf'])

    # notificar via Twilio preferencialmente, fallback para pywhatkit
    tw = enviar_twilio(cliente)
    if tw.get('erro'):
        enviar_pywhatkit(cliente)
    return {"status": "ok", "id": c.id}

_scheduler = None

def start_scheduler(app):
    global _scheduler
    if _scheduler:
        return
    scheduler = BackgroundScheduler()
    interval = app.config.get('SCHEDULER_INTERVAL_MINUTES', 30)
    # Você pode alterar job para ler CPFs de fila/arquivo
    # Aqui registramos um job de exemplo que roda para um CPF de teste
    scheduler.add_job(lambda: executar_ciclo('12345678900'), 'interval', minutes=interval, id='ciclo_padrao', replace_existing=True)
    scheduler.start()
    _scheduler = scheduler
    logger.info("Scheduler iniciado intervalo=%s minutos", interval)
