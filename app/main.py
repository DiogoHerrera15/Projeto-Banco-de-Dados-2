from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.routes import cargo_route, cliente_route  
app = FastAPI(title=settings.app_name)

app.include_router(cargo_route.router)
app.include_router(cliente_route.router) 


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:
        db_status = f"erro: {exc}"
    return {"api": "ok", "database": db_status}