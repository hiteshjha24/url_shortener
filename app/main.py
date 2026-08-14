# app/main.py

from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import engine, Base, getdb
from app.api.endpoints import router as api_router
from app.services.crud import get_url_by_short_code, increment_click_count_background

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/{short_code}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
def redirect_to_target(
    short_code: str,
    background_tasks: BackgroundTasks,    # <--- Inject BackgroundTasks
    db: Session = Depends(get_db)
):
    db_url = get_url_by_short_code(db, short_code)

    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found or inactive."
        )

    # Timezone-safe expiration check
    if db_url.expires_at:
        expires_at = db_url.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="This short URL has expired."
            )

    # Step: Schedule database write to run AFTER response is sent
    background_tasks.add_task(increment_click_count_background, short_code)

    # Return redirect immediately
    return RedirectResponse(url=db_url.target_url, status_code=status.HTTP_302_FOUND)