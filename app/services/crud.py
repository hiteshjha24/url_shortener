from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.url import URL
from app.db.session import SessionLocal
from app.schemas.url import URLCreate

def get_url_by_short_code(db: Session, short_code: str)-> URL | None:
    return db.query(URL).filter(URL.short_code == short_code, URL.is_active == True).first()

def create_url_record(
        db : Session,
        url_in: URLCreate,
        short_code: str,
        expires_at : datetime | None
)-> URL:
    db_url = URL(
        target_url = str(url_in.target_url),
        short_code = short_code,
        expires_at= expires_at
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def increment_click_count_background(short_code: str) -> None:
    """
    Background worker: Opens a dedicated DB session,
    increments clicks, and safely closes the session.
    """
    db = SessionLocal()
    try:
        db_url = db.query(URL).filter(URL.short_code == short_code).first()
        if db_url:
            db_url.clicks += 1
            db.commit()
    finally:
        db.close()


def deactivate_url_records(db: Session, db_url: URL)-> None:
    db_url.is_active = False
    db.commit()