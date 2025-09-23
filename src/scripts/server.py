import uvicorn
from fastapi import FastAPI, Request
from src.core.routers import routes
from fastapi import FastAPI, responses
from src.core.database import TORTOISE_ORM
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse





app = FastAPI(
    title="Outside OpenAPI Documentation",
    description="This is the API documentation for Project Outside solely for acknowledged developers.",
    version="1.0.0",
    contact={
        "name": "Outside",
        "url": "https://outsidelife.com/support",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit/"
    },
    openapi_tags=[
        {
            "name": "Outside",
            "description": "API for Outside"
        }
    ],
    default_response_class=responses.ORJSONResponse,
)

app.add_middleware(GZipMiddleware, minimum_size=500) 

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000',
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:5174',
        'http://127.0.0.1:5500',
        'https://www.outsidetickets.com',
        'https://www.outsidetickets.com',
        'https://outsidetickets.com'/
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return "Development Server is working"


list(map(lambda r: app.include_router(r), routes))

def run_server():
    uvicorn.run("src.scripts.server:app", host="0.0.0.0", port=8080, reload=True)


production = "gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80"