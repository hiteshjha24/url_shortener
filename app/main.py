from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.limiter import limiter
from app.db.session import engine, Base, getdb
from app.api.endpoints import router as api_router
from app.services.crud import get_url_by_short_code, increment_click_count_background
from app.services.cache import get_cached_url, set_cached_url

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)


app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": f"Rate limit exceeded: {exc.detail}"}
    )

# Include API endpoints
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/{short_code}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
def redirect_to_target(
    short_code: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(getdb)
):
    # 1. Check Redis Cache
    cached_target_url = get_cached_url(short_code)
    if cached_target_url:
        background_tasks.add_task(increment_click_count_background, short_code)
        return RedirectResponse(url=cached_target_url, status_code=status.HTTP_302_FOUND)

    # 2. Database Fallback
    db_url = get_url_by_short_code(db, short_code)
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found or inactive."
        )

    # Expiration check
    if db_url.expires_at:
        expires_at = db_url.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="This short URL has expired."
            )

    # 3. Cache & Redirect
    set_cached_url(short_code, db_url.target_url)
    background_tasks.add_task(increment_click_count_background, short_code)
    return RedirectResponse(url=db_url.target_url, status_code=status.HTTP_302_FOUND)