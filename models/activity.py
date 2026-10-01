from datetime import datetime


class DriverActivity:
    def __init__(self, driver_id, timestamp, status):
        self._driver_id = driver_id
        self._timestamp = timestamp
        self._status = status

    @property
    def driver_id(self):
        return self._driver_id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def status(self):
        return self._status

    def get_datetime(self):
        if isinstance(self._timestamp, datetime):
            return self._timestamp

        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y %H:%M"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(self._timestamp, fmt)
            except (ValueError, TypeError):
                continue

        return None

    def is_online(self):
        return self._status.lower() == "online"

    def is_offline(self):
        return self._status.lower() == "offline"

    def __repr__(self):
        return (
            f"DriverActivity("
            f"driver_id='{self._driver_id}', "
            f"timestamp='{self._timestamp}', "
            f"status='{self._status}')"
        )