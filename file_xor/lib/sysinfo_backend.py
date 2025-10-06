import platform
import psutil


def format_system_info(bot_name: str) -> str:
    uname = platform.uname()
    sys_info = (
        f"**❍⊷══〘{bot_name}〙═══⊷❍**\n\n"
        f"🖥 **System Information**\n"
        f"**System**: {uname.system}\n"
        f"**Node Name**: {uname.node}\n"
        f"**Release**: {uname.release}\n"
        f"**Version**: {uname.version}\n"
        f"**Machine**: {uname.machine}\n"
        f"**Processor**: {uname.processor}\n"
    )

    memory = psutil.virtual_memory()
    mem_info = (
        f"💾 **Memory Information**\n"
        f"**Total**: {memory.total / (1024 ** 3):.2f} GB\n"
        f"**Available**: {memory.available / (1024 ** 3):.2f} GB\n"
        f"**Used**: {memory.used / (1024 ** 3):.2f} GB\n"
        f"**Percentage**: {memory.percent}%\n"
    )

    return f"{sys_info}\n{mem_info}"
