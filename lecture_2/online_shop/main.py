from fastapi import FastAPI
from lecture_2.online_shop.api.online_shop import router


app = FastAPI()
app.include_router(router)
