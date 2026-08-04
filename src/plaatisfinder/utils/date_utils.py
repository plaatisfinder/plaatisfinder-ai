from datetime import datetime


def days_online(first_seen):

    if not first_seen:
        return None

    first = datetime.fromisoformat(first_seen)

    return (datetime.now() - first).days