from django.conf import settings
from celery import shared_task
from .models import RpgDashboard
from datetime import datetime, timedelta
from collections import Counter
import uuid
import requests
import logging

logger = logging.getLogger(__name__)

print("daily_fetch_data.py is loaded")

@shared_task
def daily_fetch_data():
    logger.info("start_task")
    try:
        logger.info("Starting daily_fetch_data task")
        current_date = datetime.now().date()
        yesterday = current_date - timedelta(days=1)
        rpg_data_provider_events_url = "{}{}{}{}{}".format(settings.RPG_DATA_PROVIDER_ENDPOINT, '/events/list_events?rpg_status=1&night_of_stay__gte=', yesterday, '&night_of_stay__lte=', yesterday)
        response = requests.get(rpg_data_provider_events_url)
        logger.info(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            rpg_data_provider_events = response.json()

            hotel_counts = Counter(item['hotel_id'] for item in rpg_data_provider_events.get('data'))
            logger.info(f"Hotel counts: {hotel_counts}")
            for hotel_id, count in hotel_counts.items():
                RpgDashboard(
                    id = uuid.uuid4(),
                    hotel_id = hotel_id,
                    period = yesterday,
                    number_of_bookings = count,
                ).save()
            logger.info("Task completed successfully")
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        # Handle any exceptions that occur during the request
        logger.info(f"Error fetching events data: {e}")