import logging
from datetime import datetime
logger = logging.getLogger(__name__)

def tratar_dados(api_data):
    if not api_data or 'erro' in api_data:
        logger.warning("Dados inválidos do API: %s", api_data)
        return {"status": "erro", "detalhe": api_data.get('erro') if api_data else 'nenhum dado'}

    cliente = {
        "nome": api_data.get("nome") or "Desconhecido",
        "cpf": api_data.get("cpf"),
        "margem": float(api_data.get("margem", 0)),
        "conta": api_data.get("tipo_conta", "N/A"),
        "data": api_data.get("data_consulta") or datetime.utcnow().isoformat(),
        "raw": str(api_data)
    }
    logger.info("Dados processados: %s", cliente["cpf"])
    return {"status": "ok", "cliente": cliente}
