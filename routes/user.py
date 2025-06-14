from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.modelo import session, User, UserDetail, PivoteUserCareer, InputUser, InputLogin, InputUserAddCareer
from sqlalchemy.orm import joinedload
from auth.security import Security

user = APIRouter()


@user.get("/")
### funcion helloUer documentacion
def helloUser():
    return "Hello User!!!"

@user.get("/users/all")
### funcion helloUer documentacion
def getAllUsers(req: Request):
    try:
        has_access = Security.verify_token(req.headers)
        if "iat" in has_access:
            usersWithDetail = session.query(User).options(joinedload(User.userdetail)).all()
            usuarios_con_detalle = []
            for user in usersWithDetail:
                user_con_detalle = {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "first_name": user.userdetail.first_name,
                    "last_name": user.userdetail.last_name,
                    "dni": user.userdetail.dni,
                    "type": user.userdetail.type,
                    "email": user.userdetail.email,
                }
                usuarios_con_detalle.append(user_con_detalle)
            return JSONResponse(status_code=200, content=usuarios_con_detalle)
        else: 
            return JSONResponse(
                status_code=401,
                content=has_access
            )
    except Exception as ex:
        print("Error ---->> ", ex)
        return {"message": "Error al obtener los usuarios"}
    
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

@user.post("/users/add")
def create_user(us: InputUser):
    try:
        newUser = User(us.username, us.password)
        newUserDetail = UserDetail(us.firstname, us.lastname, us.dni, us.type, us.email)
        newUser.userdetail = newUserDetail
        session.add(newUser)
        session.commit()
        return "Usuario creado con éxito!"
    except Exception as ex:
        session.rollback()
        print("Error ---->> ", ex)
    finally:
        session.close()
       
@user.post("/users/login")
def login_user(us: InputLogin):
    try:
        user = session.query(User).filter(User.username == us.username).first()
        if user and user.password == us.password:
            tkn = Security.generate_token(user)
            if not tkn:
                return {"message":"Error en la generación del token!"}
            else:
                res = {
                        "status": "success",
                        "token": tkn,
                        "user": user.userdetail,
                        "estado_del_tiempo":"llueve",
                        "message":"User logged in successfully!"
                    } 
                
                print(res)
                return res
        else:
            res= {"message": "Invalid username or password"}
            print(res)
            return res
    except Exception as ex:
        print("Error ---->> ", ex)
    finally:
        session.close()


## Inscribir un alumno a una carrera      
@user.post("/user/addcareer")
def addCareer(ins: InputUserAddCareer):
    try: 
        newInsc = PivoteUserCareer(ins.id_user, ins.id_career)
        session.add(newInsc)
        session.commit()
        res = f"{newInsc.user.userdetail.first_name} {newInsc.user.userdetail.last_name} fue inscripto correctamente a {newInsc.career.name}"
        print(res)
        return res
    except Exception as ex:
        session.rollback()
        print("Error al inscribir al alumno:", ex)
        import traceback
        traceback.print_exc()    
    finally:
        session.close()

@user.get("/user/career/{_username}")
def get_career_user(_username: str):
    try:
        userEncontrado = session.query(User).filter(User.username == _username ).first()
        arraySalida = []
        if(userEncontrado):
            pivoteusercareer = userEncontrado.pivoteusercareer
            for pivote in pivoteusercareer:
                career_detail = {
                    "usuario": f"{pivote.user.userdetail.first_name} {pivote.user.userdetail.last_name}",
                    "carrera": pivote.career.name,
                }
                arraySalida.append(career_detail)
            return arraySalida
        else:
            return "Usuario no encontrado!"
    except Exception as ex:
        session.rollback()
        print("Error al traer usuario y/o pagos")
    finally:
        session.close()