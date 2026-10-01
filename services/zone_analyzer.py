from collections import Counter


class ZoneAnalyzer:
    def __init__(self, trips):
        self.trips = trips

    def zones(self):
        return sorted(
            {
                trip.pickup_zone
                for trip in self.trips
            }
        )

    def total_zones(self):
        return len(self.zones())

    def trip_count_by_zone(self):
        return dict(
            Counter(
                trip.pickup_zone
                for trip in self.trips
            )
        )

    def completed_trip_count_by_zone(self):
        return dict(
            Counter(
                trip.pickup_zone
                for trip in self.trips
                if trip.is_completed()
            )
        )

    def cancelled_trip_count_by_zone(self):
        return dict(
            Counter(
                trip.pickup_zone
                for trip in self.trips
                if not trip.is_completed()
            )
        )

    def revenue_by_zone(self):
        revenue = {}

        for trip in self.trips:
            if trip.is_completed():
                revenue[trip.pickup_zone] = (
                    revenue.get(trip.pickup_zone, 0)
                    + trip.fare
                )

        return revenue

    def average_fare_by_zone(self):
        fares = {}

        for trip in self.trips:
            if trip.is_completed():
                fares.setdefault(
                    trip.pickup_zone,
                    []
                ).append(trip.fare)

        return {
            zone: sum(values) / len(values)
            for zone, values in fares.items()
        }

    def cancellation_rate_by_zone(self):
        total = self.trip_count_by_zone()
        cancelled = self.cancelled_trip_count_by_zone()

        result = {}

        for zone, count in total.items():
            result[zone] = (
                cancelled.get(zone, 0) / count
            ) * 100

        return result

    def top_zones_by_demand(self, k=5):
        counts = self.trip_count_by_zone()

        return sorted(
            counts.items(),
            key=lambda item: item[1],
            reverse=True
        )[:k]

    def top_zones_by_revenue(self, k=5):
        revenue = self.revenue_by_zone()

        return sorted(
            revenue.items(),
            key=lambda item: item[1],
            reverse=True
        )[:k]

    def zone_summary(self, zone):
        zone_trips = [
            trip
            for trip in self.trips
            if trip.pickup_zone == zone
        ]

        if not zone_trips:
            return None

        completed = [
            trip
            for trip in zone_trips
            if trip.is_completed()
        ]

        cancelled = [
            trip
            for trip in zone_trips
            if not trip.is_completed()
        ]

        revenue = sum(
            trip.fare
            for trip in completed
        )

        return {
            "zone": zone,
            "total_trips": len(zone_trips),
            "completed_trips": len(completed),
            "cancelled_trips": len(cancelled),
            "cancellation_rate": (
                len(cancelled) / len(zone_trips)
            ) * 100,
            "revenue": revenue
        }