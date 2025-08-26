import logging
from datetime import datetime

# Configure log
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f'backend_{datetime.now().strftime("%Y%m%d")}.log'
)

logger = logging.getLogger("financial_ai_debug")