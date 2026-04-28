# Instalación 
pip install -r requirements.txt
# Despliegue Puerto 8010
python -m uvicorn app.main:app --reload --port 8010
# Swagger
http://localhost:8010/docs
