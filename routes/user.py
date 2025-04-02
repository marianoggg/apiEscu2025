from fastapi import APIRouter
from models.modelo import session, User, InputUser

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

@user.get("/users/{us}/{pw}")
### funcion helloUer documentacion
def loginUser(us:str, pw:str):
    usu = session.query(User).filter(User.username==us).first()
    if usu is None:
        return "Usuario no encontrado!"
    if usu.password==pw: 
        return "Usuario logueado con éxito!"
    else:
        return "Contraseña incorrecta!"

@user.post("/users/new")
def create_user(us: InputUser):
    try:
        usu = User(us.id, us.username, us.password)
        session.add(usu)
        session.commit()
        return "Usuario creado con éxito!"
    except Exception as ex:
        print("Error ---->> ", ex)