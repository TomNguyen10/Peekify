from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from data.postgresql import SessionLocal
from models.user import User
from utils.spotify_tokens import refresh_spotify_token
import logging
from datetime import datetime
from pytz import timezone

logging.basicConfig(level=logging.INFO)

est = timezone('US/Eastern')


def refresh_all_tokens():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            try:
                refreshed_token = refresh_spotify_token(db, user.user_id)
                if refreshed_token:
                    logging.info(f"Token refreshed for user {user.user_id}")
                else:
                    logging.warning(
                        f"Failed to refresh token for user {user.user_id}")
            except Exception as e:
                logging.error(f"Error refreshing token for user {
                              user.user_id}: {str(e)}")
    finally:
        db.close()
    logging.info(f"Token Refresh job executed at {datetime.now(est)}")


def setup_scheduler():
    scheduler = BackgroundScheduler()

    # Token refresh job (runs at 11:30 PM, 5:30 AM, 11:30 AM, 5:30 PM EST)
    scheduler.add_job(refresh_all_tokens, CronTrigger(
        hour="2,5,8,11,14,17,20,23", minute="30", timezone=est))

    return scheduler
