from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine(
    "sqlite:///./app.db", 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()