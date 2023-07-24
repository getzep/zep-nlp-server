import uvicorn

from app.api import app
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=settings.server_port, log_level=settings.log_level
    )
