class InsightsEngine:

    def __init__(
        self,
        driver_analyzer,
        trip_analyzer,
        zone_analyzer,
        utilization_analyzer,
        peak_analyzer,
        anomaly_detector
    ):
        self.driver_analyzer = driver_analyzer
        self.trip_analyzer = trip_analyzer
        self.zone_analyzer = zone_analyzer
        self.utilization_analyzer = utilization_analyzer
        self.peak_analyzer = peak_analyzer
        self.anomaly_detector = anomaly_detector

    def generate_insights(self):
        insights = []

        trip_summary = self.trip_analyzer.trip_summary()

        total_trips = trip_summary["total_trips"]
        completed_trips = trip_summary["completed_trips"]
        cancelled_trips = trip_summary["cancelled_trips"]

        if total_trips > 0:
            cancellation_rate = (
                cancelled_trips / total_trips
            ) * 100

            if cancellation_rate >= 20:
                insights.append(
                    f"Cancellation rate is "
                    f"{cancellation_rate:.1f}%, indicating "
                    f"a significant level of trip cancellations."
                )

        top_drivers = (
            self.driver_analyzer.top_drivers_by_revenue(3)
        )

        if top_drivers:
            driver_id, revenue = top_drivers[0]

            insights.append(
                f"Driver {driver_id} generated the highest "
                f"revenue of ₹{revenue:.0f}."
            )

        top_zones = (
            self.zone_analyzer.top_zones_by_demand(3)
        )

        if top_zones:
            zone, demand = top_zones[0]

            insights.append(
                f"{zone} has the highest trip demand "
                f"with {demand} trips."
            )

        peak_hour = (
            self.peak_analyzer.peak_demand_hour()
        )

        if peak_hour:
            hour, demand = peak_hour

            insights.append(
                f"Peak demand occurs around {hour}:00 "
                f"with {demand} trip requests."
            )

        utilization = (
            self.utilization_analyzer.driver_utilization()
        )

        if utilization:
            highest_idle = max(
                utilization.items(),
                key=lambda item: item[1]["idle_hours"]
            )

            driver_id = highest_idle[0]
            idle_hours = highest_idle[1]["idle_hours"]

            insights.append(
                f"Driver {driver_id} has the highest "
                f"idle time at {idle_hours:.2f} hours."
            )

        anomalies = (
            self.anomaly_detector.detect_all()
        )

        high_fare_count = len(
            anomalies["high_fare_trips"]
        )

        long_distance_count = len(
            anomalies["long_distance_trips"]
        )

        long_duration_count = len(
            anomalies["long_duration_trips"]
        )

        if high_fare_count > 0:
            insights.append(
                f"{high_fare_count} high-fare trip(s) "
                f"were detected."
            )

        if long_distance_count > 0:
            insights.append(
                f"{long_distance_count} long-distance "
                f"trip(s) were detected."
            )

        if long_duration_count > 0:
            insights.append(
                f"{long_duration_count} long-duration "
                f"trip(s) were detected."
            )

        if not insights:
            insights.append(
                "No significant operational insights "
                "were detected."
            )

        return insights