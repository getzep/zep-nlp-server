import uvicorn

from app.api import app
from app.config import settings

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = settings.log_format

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.server_port,
        log_level=settings.log_level,
        log_config=log_config,
    )
