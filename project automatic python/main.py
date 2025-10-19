import os
from app import create_app
from app.tasks import start_scheduler
from app.auth import create_admin
from app.banco import session
import logging

app = create_app()
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # criar admin inicial (troque depois)
    admin_user = os.getenv('INITIAL_ADMIN_USER', 'admin')
    admin_pass = os.getenv('INITIAL_ADMIN_PASS', 'admin123')
    try:
        create_admin(admin_user, admin_pass)
    except Exception as e:
        logger.exception("Erro ao criar admin (talvez já exista)")

    # start scheduler
    start_scheduler(app)

    # rodar Flask (em produção use gunicorn)
    app.run(host='0.0.0.0', port=8080)
