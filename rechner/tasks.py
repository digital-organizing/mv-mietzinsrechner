from core.celery import app
from rechner import datasource


@app.task
def update_price_db():
    datasource.update_price_db()
