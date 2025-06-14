import datetime, pytz, jwt


class Security:
    secret = "pepito"

    @classmethod
    def hoy(cls):
        return datetime.datetime.now(pytz.timezone("America/Buenos_Aires"))


    @classmethod
    def generate_token(cls, authUser):
        payload = {
            "iat": cls.hoy(),
            "exp": cls.hoy() + datetime.timedelta(minutes=480),
            "username": authUser.username,
        }
        try:
            return jwt.encode(payload, cls.secret, algorithm="HS256")
        except Exception:
            return None
    

    @classmethod
    def verify_token(cls, headers):
        if headers["authorization"]:
            try:
                tkn = headers["authorization"].split(" ")[1]
                payload = jwt.decode(tkn, cls.secret, algorithms=["HS256"])
                return payload
            except jwt.ExpiredSignatureError:
                return {"success": False, "message": "Token expired!"}
            except jwt.InvalidSignatureError:
                return {"success": False, "message": "Token: signature error!"}
            except jwt.DecodeError as e:
                return {"success": False, "message": "Invalid token!"}
            except Exception as e:
                return {"success": False, "message": "Token: unknown error!"}
        else:
            return {"success": False, "message": "Authorization header missing!"}
