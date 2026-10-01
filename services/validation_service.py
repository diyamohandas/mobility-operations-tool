import csv


class DataValidator:
    REQUIRED_COLUMNS = {
        "drivers": {
            "driver_id",
            "driver_name",
            "city",
            "vehicle_type",
            "rating",
            "status"
        },
        "trips": {
            "trip_id",
            "driver_id",
            "rider_id",
            "city",
            "pickup_zone",
            "drop_zone",
            "request_time",
            "pickup_time",
            "drop_time",
            "distance_km",
            "fare",
            "status",
            "cancellation_reason"
        },
        "activities": {
            "driver_id",
            "timestamp",
            "status"
        }
    }

    def validate_file(self, file_path, dataset_type):
        if dataset_type not in self.REQUIRED_COLUMNS:
            return False, "Invalid dataset type."

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    return False, "CSV file is empty or has no header."

                actual_columns = set(reader.fieldnames)
                required_columns = self.REQUIRED_COLUMNS[dataset_type]

                missing_columns = required_columns - actual_columns

                if missing_columns:
                    return (
                        False,
                        f"Missing required columns: {sorted(missing_columns)}"
                    )

                rows = list(reader)

                if not rows:
                    return False, "CSV file contains no data rows."

                return True, "Validation successful."

        except FileNotFoundError:
            return False, "File not found."

        except UnicodeDecodeError:
            return False, "File must be UTF-8 encoded."

        except csv.Error:
            return False, "Invalid CSV format."

    def validate_all(self, drivers_path, trips_path, activities_path):
        results = {}

        results["drivers"] = self.validate_file(
            drivers_path,
            "drivers"
        )

        results["trips"] = self.validate_file(
            trips_path,
            "trips"
        )

        results["activities"] = self.validate_file(
            activities_path,
            "activities"
        )

        return results

    def is_valid(self, file_path, dataset_type):
        valid, _ = self.validate_file(
            file_path,
            dataset_type
        )

        return valid