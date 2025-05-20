from fastapi import FastAPI
import uvicorn

from app.api.routes import api_router


app = FastAPI()


app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="127.1.1.1", port=8001)
