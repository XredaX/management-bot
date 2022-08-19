import os
class Config:
    BOT_TOKEN = str(os.environ.get('BOT_TOKEN', None))
    ADMIN_ID = str(os.environ.get('ADMIN_ID', None))
    SPOT_ID = str(os.environ.get('SPOT_ID', None))
    FUTURE_ID = str(os.environ.get('FUTURE_ID', None))
