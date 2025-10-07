from pathlib import Path
from file_xor.lib.url_utils import normalize_base_url


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def save_host_url(url: str) -> bool:
    base = normalize_base_url(url)
    if not base:
        return False

    runtime_path = _project_root() / "runtime.py"
    content = (
        "# Auto-generated at runtime. Do not edit manually.\n"
        f"HOST_URL = \"{base}\"\n"
    )

    try:
        if runtime_path.exists():
            try:
                existing = runtime_path.read_text(encoding="utf-8")
            except Exception:
                existing = ""
            if existing == content:
                return True
        runtime_path.write_text(content, encoding="utf-8")
        return True
    except Exception:
        # Silently ignore failures; app should continue without crashing
        return False


def load_host_url() -> str:
    try:
        from importlib import import_module
        runtime = import_module("runtime")
        host = getattr(runtime, "HOST_URL", "")
        return str(host).strip()
    except Exception:
        return ""
