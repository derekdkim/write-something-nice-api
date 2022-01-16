"""Pydantic Data Validation Library"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Schema for environment variables. 
    Reads variables in .env located in the project root.
    The variables must follow this schema with key names being in all caps.
    """

    pg_username: str
    pg_password: str
    pg_port: str
    pg_db_name: str
    secret_key: str
    bcrypt_algorithm: str
    jwt_exp_minutes: str

    class Config:
        """Reads .env file"""

        env_file = ".env"


env = Settings()