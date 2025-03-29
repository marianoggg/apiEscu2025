from fastapi import APIRouter
from models.modelo import session, User

user = APIRouter()


@user.get("/")
### funcion helloUer documentacion
def helloUser():
    return "Hello User!!!"

@user.get("/users/all")
### funcion helloUer documentacion
def getAllUsers():
    try: 
        return session.query(User).all()
    except Exception as ex:
        print("Error ---->> ", ex)