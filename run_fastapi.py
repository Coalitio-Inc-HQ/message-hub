import uvicorn
from src.fastapi_app import app

uvicorn.run(app, host="127.0.0.1", port=8000)
# 0.0.0.0 для docker