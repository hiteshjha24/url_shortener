from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.services.cache import delete_cached_url
from app.db.session import getdb
from app.schemas.url import URLCreate, URLResponse, URLStats
from app.services.crud import (
    get_url_by_short_code,
    create_url_record,
    increment_click_count_background,
    deactivate_url_records,
)
from app.services.shortener import generate_random_code, calculate_expiration_date

router = APIRouter()


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(
    url_in: URLCreate,
    request: Request,
    db: Session = Depends(getdb)
):
    if url_in.custom_alias:
        existing_url = get_url_by_short_code(db, url_in.custom_alias)
        if existing_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This custom alias is already in use."
            )
        short_code = url_in.custom_alias
    else:
        for _ in range(5):
            candidate = generate_random_code(length=6)
            if not get_url_by_short_code(db, candidate):
                short_code = candidate
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to generate unique short code. Please try again."
            )

    expires_at = calculate_expiration_date(url_in.expires_in_days)

    db_url = create_url_record(db, url_in, short_code, expires_at)

    base_url = str(request.base_url).rstrip("/")
    return URLResponse(
        target_url=db_url.target_url,
        short_code=db_url.short_code,
        short_url=f"{base_url}/{db_url.short_code}",
        created_at=db_url.created_at,
        expires_at=db_url.expires_at,
        is_active=db_url.is_active,
    )


@router.get("/stats/{short_code}", response_model=URLStats)
def get_url_statistics(
    short_code: str,
    request: Request,
    db: Session = Depends(getdb)
):
    db_url = get_url_by_short_code(db, short_code)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found."
        )

    base_url = str(request.base_url).rstrip("/")
    return URLStats(
        target_url=db_url.target_url,
        short_code=db_url.short_code,
        short_url=f"{base_url}/{db_url.short_code}",
        created_at=db_url.created_at,
        expires_at=db_url.expires_at,
        is_active=db_url.is_active,
        clicks=db_url.clicks,
    )


@router.delete("/shorten/{short_code}", status_code=status.HTTP_200_OK)
def delete_short_url(short_code: str, db: Session = Depends(getdb)):
    db_url = get_url_by_short_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found.")

    deactivate_url_records(db, db_url)
    delete_cached_url(short_code)  # <--- Invalidate Redis cache!
    return {"message": f"Short URL '{short_code}' has been deactivated successfully."}