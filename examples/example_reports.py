from ga4_connector import GA4ReportConfig, GA4Reporter

PROPERTY_ID = "543114448"
START_DATE = "yesterday"  # Use "yesterday" for production reporting.
END_DATE = "today" # Use "today" for test and dev.

def main():
    config = GA4ReportConfig(
        property_id=PROPERTY_ID,
        start_date=START_DATE,
        end_date=END_DATE,
        limit=50,
    )

    reporter = GA4Reporter(config)

    print("\nExample 1: Active users by country and city")
    print(reporter.active_users_by_country())

    print("\nExample 2: Event counts by event name")
    print(reporter.event_counts_by_event_name())


if __name__ == "__main__":
    main()