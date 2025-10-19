import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)

def consultar_facta(cpf):
    api_key = current_app.config.get('FACTA_API_KEY')
    if not api_key:
        logger.error("FACTA_API_KEY não configurada")
        return {"erro": "API_KEY ausente"}

    url = f"https://api.facta.exemplo/consulta"  # substitua URL real
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"cpf": cpf}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        logger.info("Consulta FACTA OK para %s", cpf)
        return data
    except requests.RequestException as e:
        logger.exception("Erro ao consultar FACTA")
        return {"erro": str(e)}
