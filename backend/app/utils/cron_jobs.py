from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from data.postgresql import SessionLocal
from models.user import User
from utils.spotify_tokens import refresh_spotify_token, get_spotify_token
from utils.user_listening_activity import fetch_and_store_recent_user_activity
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
                refreshed_token = refresh_spotify_token(db, user.id)
                if refreshed_token:
                    logging.info(f"Token refreshed for user {user.id}")
                else:
                    logging.warning(
                        f"Failed to refresh token for user {user.id}")
            except Exception as e:
                logging.error(f"""Error refreshing token for user {
                              user.id}: {str(e)}""")
    finally:
        db.close()
    logging.info(f"Token Refresh job executed at {datetime.now(est)}")


def test_fetch_and_store_for_all_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            try:
                token = get_spotify_token(db, user.id)
                access_token = token.access_token if token else None
                if not access_token:
                    logging.warning(
                        f"No access token found for user {user.id}")
                    continue

                logging.info(
                    f"Fetching and storing recent activity for user {user.id}")
                activities = fetch_and_store_recent_user_activity(
                    db, user.id, access_token)
                logging.info(f"""Stored {len(activities)
                                         } new activities for user {user.id}""")

            except Exception as e:
                logging.error(f"Error processing user {user.id}: {str(e)}")
    finally:
        db.close()


def setup_scheduler():
    scheduler = BackgroundScheduler()

    # Token refresh job (runs at 2:30 AM, 5:30 AM, 8:30 AM, 11:30 AM, 2:30 PM, 5:30 PM, 8:30 PM, 11:30 PM EST)
    scheduler.add_job(refresh_all_tokens, CronTrigger(
        hour="2,5,8,11,14,17,20,22,23", minute="30", timezone=est))
    scheduler.add_job(test_fetch_and_store_for_all_users, CronTrigger(
        hour="0,3,6,9,12,15,18,21,22", minute="31", timezone=est))
    return scheduler
