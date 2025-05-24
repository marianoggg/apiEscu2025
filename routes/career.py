from fastapi import APIRouter
from models.modelo import Career, InputCareer, session

career = APIRouter()

@career.get("/career/all")
def get_careers():
    return session.query(Career).all()

@career.post("/career/add")
def add_career(ca: InputCareer):
    try:
        newCareer = Career(ca.name)
        session.add(newCareer)
        session.commit()
        res = f"carrera {ca.name} guardada correctamente!"
        print(res)
        return res
    except Exception as ex:
        session.rollback()
        print("Error al agregar career --> ", ex) 
    finally:
        session.close()
