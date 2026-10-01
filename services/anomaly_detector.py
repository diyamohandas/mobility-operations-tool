from collections import Counter
from datetime import datetime


class AnomalyDetector:

    def __init__(self, trips, drivers):
        self.trips = trips
        self.drivers = drivers

    def _parse_datetime(self, value):
        if isinstance(value, datetime):
            return value

        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        )

    def high_fare_trips(self, threshold=500):
        return [
            trip
            for trip in self.trips
            if trip.fare > threshold
        ]

    def long_distance_trips(self, threshold=15):
        return [
            trip
            for trip in self.trips
            if trip.distance_km > threshold
        ]

    def long_duration_trips(self, threshold_minutes=60):
        result = []

        for trip in self.trips:
            if not trip.is_completed():
                continue

            pickup_time = self._parse_datetime(
                trip.pickup_time
            )

            drop_time = self._parse_datetime(
                trip.drop_time
            )

            duration_minutes = (
                drop_time - pickup_time
            ).total_seconds() / 60

            if duration_minutes > threshold_minutes:
                result.append(trip)

        return result

    def driver_cancellation_anomalies(
        self,
        threshold=2
    ):
        counts = Counter()

        for trip in self.trips:
            if (
                not trip.is_completed()
                and trip.cancellation_reason
                and "Driver" in trip.cancellation_reason
            ):
                counts[trip.driver_id] += 1

        return {
            driver_id: count
            for driver_id, count in counts.items()
            if count >= threshold
        }

    def zone_cancellation_anomalies(
        self,
        threshold=50
    ):
        total = Counter()
        cancelled = Counter()

        for trip in self.trips:
            zone = trip.pickup_zone

            total[zone] += 1

            if not trip.is_completed():
                cancelled[zone] += 1

        result = {}

        for zone, count in total.items():
            rate = (
                cancelled[zone] / count
            ) * 100

            if rate >= threshold:
                result[zone] = rate

        return result

    def detect_all(self):
        return {
            "high_fare_trips": self.high_fare_trips(),
            "long_distance_trips": self.long_distance_trips(),
            "long_duration_trips": self.long_duration_trips(),
            "driver_cancellation_anomalies":
                self.driver_cancellation_anomalies(),
            "zone_cancellation_anomalies":
                self.zone_cancellation_anomalies()
        }