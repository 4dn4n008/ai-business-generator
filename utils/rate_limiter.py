from config import Config


def can_generate(session) -> bool:
    usage_count = session.get("usage_count", 0)
    return usage_count < Config.MAX_FREE_GENERATIONS


def increment_usage(session) -> None:
    session["usage_count"] = session.get("usage_count", 0) + 1


def get_remaining(session) -> int:
    used = session.get("usage_count", 0)
    return max(0, Config.MAX_FREE_GENERATIONS - used)
