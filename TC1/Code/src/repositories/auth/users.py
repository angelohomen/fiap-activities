from passlib.context import CryptContext

class Users:
    @classmethod
    def get_user(cls, pwd_context: CryptContext, username: str):
        return cls.get_all_users(pwd_context).get(username)

    @staticmethod
    def get_all_users(pwd_context: CryptContext):
        return {
            "string": {
                "username": "string",
                "full_name": "string",
                "email": "string",
                "hashed_password": pwd_context.hash("string"),
                "disabled": False,
            }
        }