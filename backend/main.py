"""
main.py
Application entry point. Run with: python main.py  OR  uvicorn main:app
"""
import uvicorn

from api.app import create_app
from core.config import get_settings

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=not settings.is_production,
        log_config=None,  # structlog handles logging
    )
