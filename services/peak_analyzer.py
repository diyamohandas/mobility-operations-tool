from collections import Counter
from datetime import datetime


class PeakAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def _get_hour(self, request_time):
        if isinstance(request_time, datetime):
            return request_time.hour

        return datetime.strptime(
            request_time,
            "%Y-%m-%d %H:%M:%S"
        ).hour

    def demand_by_hour(self):
        counts = Counter()

        for trip in self.trips:
            hour = self._get_hour(trip.request_time)
            counts[hour] += 1

        return dict(sorted(counts.items()))

    def completed_demand_by_hour(self):
        counts = Counter()

        for trip in self.trips:
            if trip.is_completed():
                hour = self._get_hour(trip.request_time)
                counts[hour] += 1

        return dict(sorted(counts.items()))

    def cancelled_demand_by_hour(self):
        counts = Counter()

        for trip in self.trips:
            if not trip.is_completed():
                hour = self._get_hour(trip.request_time)
                counts[hour] += 1

        return dict(sorted(counts.items()))

    def peak_demand_hour(self):
        demand = self.demand_by_hour()

        if not demand:
            return None

        return max(
            demand.items(),
            key=lambda item: item[1]
        )

    def top_demand_hours(self, k=5):
        demand = self.demand_by_hour()

        return sorted(
            demand.items(),
            key=lambda item: item[1],
            reverse=True
        )[:k]

    def cancellation_rate_by_hour(self):
        total = Counter()
        cancelled = Counter()

        for trip in self.trips:
            hour = self._get_hour(trip.request_time)

            total[hour] += 1

            if not trip.is_completed():
                cancelled[hour] += 1

        result = {}

        for hour, count in total.items():
            result[hour] = (
                cancelled[hour] / count
            ) * 100

        return dict(sorted(result.items()))

    def peak_cancellation_hour(self):
        rates = self.cancellation_rate_by_hour()

        if not rates:
            return None

        return max(
            rates.items(),
            key=lambda item: item[1]
        )

    def cancellation_reasons(self):
        return dict(
            Counter(
                trip.cancellation_reason
                for trip in self.trips
                if not trip.is_completed()
                and trip.cancellation_reason
            )
        )

    def highest_cancellation_reason(self):
        reasons = self.cancellation_reasons()

        if not reasons:
            return None

        return max(
            reasons.items(),
            key=lambda item: item[1]
        )

    def cancellation_summary(self):
        cancelled = [
            trip
            for trip in self.trips
            if not trip.is_completed()
        ]

        total = len(self.trips)

        return {
            "total_trips": total,
            "cancelled_trips": len(cancelled),
            "cancellation_rate": (
                len(cancelled) / total * 100
                if total
                else 0
            ),
            "reasons": self.cancellation_reasons()
        }