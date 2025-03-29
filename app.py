from fastapi import FastAPI
from routes.user import user

api_escu = FastAPI()

api_escu.include_router(user)

