import os

import boto3
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

session = boto3.Session(region_name="us-east-1")
client = session.client("rds")

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://"
    "?ssl_ca=/usr/local/share/ca-certificates/global-bundle.pem"
    "&ssl_check_hostname=false"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@event.listens_for(engine, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    token = client.generate_db_auth_token(
        DBHostname=os.environ["ENDPOINT"],
        Port=3306,
        DBUsername=os.environ["DB_USER"],
        Region=os.environ["REGION"],
    )
    cparams["host"] = os.environ["HOST"]
    cparams["port"] = os.environ["PORT"]
    cparams["user"] = os.environ["DB_USER"]
    cparams["password"] = token
    cparams["database"] = os.environ["DATABASE"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
