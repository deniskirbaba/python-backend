from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from lecture_2.online_shop.api.online_shop import router

app = FastAPI()
app.include_router(router)

# Initialize and expose the /metrics endpoint
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
