from collections import Counter


class TripAnalyzer:
    def __init__(self, trips):
        self.trips = trips

    def total_trips(self):
        return len(self.trips)

    def completed_trips(self):
        return [
            trip
            for trip in self.trips
            if trip.is_completed()
        ]

    def cancelled_trips(self):
        return [
            trip
            for trip in self.trips
            if not trip.is_completed()
        ]

    def completed_trip_count(self):
        return len(self.completed_trips())

    def cancelled_trip_count(self):
        return len(self.cancelled_trips())

    def completion_rate(self):
        if not self.trips:
            return 0

        return (
            self.completed_trip_count()
            / len(self.trips)
        ) * 100

    def cancellation_rate(self):
        if not self.trips:
            return 0

        return (
            self.cancelled_trip_count()
            / len(self.trips)
        ) * 100

    def total_revenue(self):
        return sum(
            trip.fare
            for trip in self.trips
            if trip.is_completed()
        )

    def average_fare(self):
        completed = self.completed_trips()

        if not completed:
            return 0

        return sum(
            trip.fare
            for trip in completed
        ) / len(completed)

    def total_distance(self):
        return sum(
            trip.distance_km
            for trip in self.completed_trips()
        )

    def average_trip_distance(self):
        completed = self.completed_trips()

        if not completed:
            return 0

        return sum(
            trip.distance_km
            for trip in completed
        ) / len(completed)

    def cancellation_reasons(self):
        return dict(
            Counter(
                trip.cancellation_reason
                for trip in self.cancelled_trips()
                if trip.cancellation_reason
            )
        )

    def trips_by_city(self):
        return dict(
            Counter(
                trip.city
                for trip in self.trips
            )
        )

    def completed_trips_by_city(self):
        return dict(
            Counter(
                trip.city
                for trip in self.completed_trips()
            )
        )

    def revenue_by_city(self):
        revenue = {}

        for trip in self.completed_trips():
            revenue[trip.city] = (
                revenue.get(trip.city, 0)
                + trip.fare
            )

        return revenue

    def top_cities_by_trips(self, k=5):
        city_counts = self.trips_by_city()

        return sorted(
            city_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )[:k]

    def trip_summary(self):
        return {
            "total_trips": self.total_trips(),
            "completed_trips": self.completed_trip_count(),
            "cancelled_trips": self.cancelled_trip_count(),
            "completion_rate": self.completion_rate(),
            "cancellation_rate": self.cancellation_rate(),
            "total_revenue": self.total_revenue(),
            "average_fare": self.average_fare(),
            "total_distance": self.total_distance(),
            "average_trip_distance": self.average_trip_distance()
        }