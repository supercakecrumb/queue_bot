import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("BOT_TOKEN")
# Comma-separated Telegram user IDs allowed to clear the shared queue.
admin_user_ids = {int(value.strip()) for value in os.environ.get("ADMIN_USER_IDS", "").split(",") if value.strip()}
