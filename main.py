import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.book import router as book_router
from api.record import router as record_router
from api.user import router as user_router
from config import config

app = FastAPI()
app.include_router(user_router)
app.include_router(book_router)
app.include_router(record_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "The page you are looking for is not found."},
        )

    if exc.status_code == 422:
        return JSONResponse(
            status_code=422, content={"message": "The request body is invalid."}
        )

    if exc.status_code == 500:
        return JSONResponse(
            status_code=500,
            content={"message": "Something bad happened to the server : ("},
        )


if __name__ == "__main__":
    uvicorn.run(
        f"{__name__}:app",
        host=config.host,
        port=int(config.port),
        reload=True,
        log_level="info",
    )
