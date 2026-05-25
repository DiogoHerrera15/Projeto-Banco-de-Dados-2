from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.routes import (
    cargo_router,
    cliente_router,
    produto_router,
    transportadora_router,
    vendedor_router,
    procedure_router,
    view_router,
    trigger_router,
)

app = FastAPI(title=settings.app_name)

app.include_router(cargo_router.router)
app.include_router(cliente_router.router)
app.include_router(transportadora_router.router)
app.include_router(vendedor_router.router)
app.include_router(produto_router.router)
app.include_router(procedure_router.router)
app.include_router(view_router.router)
app.include_router(trigger_router.router)


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:
        db_status = f"erro: {exc}"
    return {"api": "ok", "database": db_status}