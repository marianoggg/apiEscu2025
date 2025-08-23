from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from models.modelo import (
    session,
    User,
    UserDetail,
    PivoteUserCareer,
    InputUser,
    InputLogin,
    InputUserAddCareer,
    InputPaginatedRequest,
    InputPaginatedRequestFilter,
    # AsyncSessionLocal,
)
from sqlalchemy import select
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
            usersWithDetail = (
                session.query(User).options(joinedload(User.userdetail)).all()
            )
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
            return JSONResponse(status_code=401, content=has_access)
    except Exception as ex:
        print("Error ---->> ", ex)
        return {"message": "Error al obtener los usuarios"}


""" @user.post("/users/paginated")
### funcion helloUer documentacion
def getUsersPaginated(
    req: Request,
    body: InputUsersPaginatedRequest,
):
    try:
        has_access = Security.verify_token(req.headers)

        if "iat" not in has_access:
            return JSONResponse(status_code=401, content=has_access)

        limit = body.limit
        last_seen_id = body.last_seen_id

        query = (
            session.query(User).options(joinedload(User.userdetail)).order_by(User.id)
        )

        if last_seen_id is not None:
            query = query.filter(User.id > last_seen_id)

        usersWithDetail = query.limit(limit).all()

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

        next_cursor = (
            usuarios_con_detalle[-1]["id"]
            if len(usuarios_con_detalle) == limit
            else None
        )

        return JSONResponse(
            status_code=200,
            content={"users": usuarios_con_detalle, "next_cursor": next_cursor},
        )
    except Exception as ex:
        print("Error al obtener página de usuarios---->> ", ex)
        return JSONResponse(
            status_code=500,
            content={"message": "Error al obtener página de usuarios"},
        )
 """


@user.get("/users/{us}/{pw}")
### funcion helloUer documentacion
def loginUser(us: str, pw: str):
    usu = session.query(User).filter(User.username == us).first()
    if usu is None:
        return "Usuario no encontrado!"
    if usu.password == pw:
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
                print(user.username)
                return {"message": "Error en la generación del token!"}
            else:
                res = {
                    "status": "success",
                    "token": tkn,
                    "user": user.userdetail,
                    "estado_del_tiempo": "llueve",
                    "message": "User logged in successfully!",
                }

                print(res)
                return res
        else:
            res = {"message": "Invalid username or password"}
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
        userEncontrado = session.query(User).filter(User.username == _username).first()
        arraySalida = []
        if userEncontrado:
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


@user.post("/user/paginated")
async def get_users_paginated(req: Request, body: InputPaginatedRequest):
    try:
        has_access = Security.verify_token(req.headers)
        if "iat" not in has_access:
            return JSONResponse(status_code=401, content=has_access)

        limit = body.limit
        last_seen_id = body.last_seen_id

        query = (
            session.query(User).options(joinedload(User.userdetail)).order_by(User.id)
        )

        if last_seen_id is not None:
            query = query.filter(User.id > last_seen_id)

        users_with_detail = query.limit(limit)

        usuarios_con_detalles = []
        for us in users_with_detail:
            user_con_detalle = {
                "id": us.id,
                "username": us.username,
                "first_name": us.userdetail.first_name,
                "last_name": us.userdetail.last_name,
                "dni": us.userdetail.dni,
                "type": us.userdetail.type,
                "email": us.userdetail.email,
            }
            usuarios_con_detalles.append(user_con_detalle)

        next_cursor = (
            usuarios_con_detalles[-1]["id"]
            if len(usuarios_con_detalles) == limit
            else None
        )

        return JSONResponse(
            status_code=200,
            content={"users": usuarios_con_detalles, "next_cursor": next_cursor},
        )

    except Exception as error:
        print("Error al obtener página de usuarios ----> ", error)
        return JSONResponse(
            status_code=500, content={"message": "Error al obtener página de usuarios"}
        )


# ruta paginated filtered con funcion sincronica
""" @user.post("/user/paginated/filtered")
def get_users_paginated_filtered(req: Request, body: InputPaginatedRequestFilter):
    try:
        has_access = Security.verify_token(req.headers)
        if "iat" not in has_access:
            return JSONResponse(status_code=401, content=has_access)

        limit = body.limit
        last_seen_id = body.last_seen_id

        query = (
            session.query(User).options(joinedload(User.userdetail)).order_by(User.id)
        )

        # 🔹 Filtros adicionales
        if hasattr(body, "filters") and body.filters:
            if "username" in body.filters:
                query = query.filter(
                    User.username.ilike(f"%{body.filters['username']}%")
                )
            if "type" in body.filters:
                query = query.filter(User.userdetail.type == body.filters["type"])
            if "email" in body.filters:
                query = query.filter(
                    User.userdetail.email.ilike(f"%{body.filters['email']}%")
                )

        # 🔹 Filtro por cursor
        if last_seen_id is not None:
            query = query.filter(User.id > last_seen_id)

        users_with_detail = query.limit(limit)

        usuarios_con_detalles = []
        for us in users_with_detail:
            user_con_detalle = {
                "id": us.id,
                "username": us.username,
                "first_name": us.userdetail.first_name,
                "last_name": us.userdetail.last_name,
                "dni": us.userdetail.dni,
                "type": us.userdetail.type,
                "email": us.userdetail.email,
            }
            usuarios_con_detalles.append(user_con_detalle)

        next_cursor = (
            usuarios_con_detalles[-1]["id"]
            if len(usuarios_con_detalles) == limit
            else None
        )

        return JSONResponse(
            status_code=200,
            content={"users": usuarios_con_detalles, "next_cursor": next_cursor},
        )

    except Exception as error:
        print("Error al obtener página de usuarios ----> ", error)
        return JSONResponse(
            status_code=500, content={"message": "Error al obtener página de usuarios"}
        )
 """

# ruta paginated filtered con funcion async


""" @user.post("/user/paginated/filtered/async")
async def get_users_paginated_filtered_async(
    req: Request, body: InputPaginatedRequestFilter
):
    try:
        has_access = Security.verify_token(req.headers)
        if "iat" not in has_access:
            return JSONResponse(status_code=401, content=has_access)

        limit = body.limit
        last_seen_id = body.last_seen_id

        async with AsyncSessionLocal() as session:

            # Construcción de la consulta
            stmt = select(User).options(joinedload(User.userdetail)).order_by(User.id)

            # Filtros adicionales
            if hasattr(body, "filters") and body.filters:
                if "username" in body.filters:
                    stmt = stmt.filter(
                        User.username.ilike(f"%{body.filters['username']}%")
                    )
                if "type" in body.filters:
                    stmt = stmt.filter(User.userdetail.type == body.filters["type"])
                if "email" in body.filters:
                    stmt = stmt.filter(
                        User.userdetail.email.ilike(f"%{body.filters['email']}%")
                    )

            # Filtro por cursor
            if last_seen_id is not None:
                stmt = stmt.filter(User.id > last_seen_id)

            # Limito resultados
            stmt = stmt.limit(limit)

            # Ejecuto la consulta
            result = await session.execute(stmt)
            users_with_detail = result.scalars().all()

            # Armo la salida de datos
            usuarios_con_detalles = [
                {
                    "id": us.id,
                    "username": us.username,
                    "first_name": us.userdetail.first_name,
                    "last_name": us.userdetail.last_name,
                    "dni": us.userdetail.dni,
                    "type": us.userdetail.type,
                    "email": us.userdetail.email,
                }
                for us in users_with_detail
            ]

            # armo la salida del cursor
            next_cursor = (
                usuarios_con_detalles[-1]["id"]
                if len(usuarios_con_detalles) == limit
                else None
            )

            # respondo con datos y cursor
            return JSONResponse(
                status_code=200,
                content={"users": usuarios_con_detalles, "next_cursor": next_cursor},
            )

    except Exception as error:
        print("Error al obtener página de usuarios ----> ", error)
        return JSONResponse(
            status_code=500, content={"message": "Error al obtener página de usuarios"}
        )
 """
