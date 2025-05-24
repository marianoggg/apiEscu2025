import sys
sys.tracebacklimit = 1
from fastapi import FastAPI
from routes.user import user
from routes.career import career
from routes.payment import payment
from fastapi.middleware.cors import CORSMiddleware

api_escu = FastAPI()

api_escu.include_router(user)
api_escu.include_router(career)
api_escu.include_router(payment)

api_escu.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

