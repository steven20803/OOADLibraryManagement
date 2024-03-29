import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from config import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True, log_level="info")
