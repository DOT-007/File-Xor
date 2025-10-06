import time
import psutil
from datetime import timedelta


def get_system_stats(bot_name: str) -> str:
    """Return a formatted stats string containing CPU, RAM and uptime."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))

    response = f"**{bot_name} **\n\n"
    response += f"**System Stats:**\n"
    response += f"**🖥️ CPU Usage:** {cpu_usage}%\n"
    response += f"**📈 RAM Usage:** {ram_usage}%\n"
    response += f"**⏳ Uptime:** {uptime_str}\n"

    return response
