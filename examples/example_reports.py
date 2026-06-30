from ga4_connector.connector import GA4Connector

PROPERTY_ID = "543114448"


def active_users_by_country(connector: GA4Connector):
    """Example 1: active users grouped by country."""
    return connector.run_report(
        dimensions=["country"],
        metrics=["activeUsers"],
        start_date="today",
        end_date="today",
    )


def event_counts_by_event_name(connector: GA4Connector):
    """Example 2: event counts grouped by event name."""
    return connector.run_report(
        dimensions=["eventName"],
        metrics=["eventCount"],
        start_date="today",
        end_date="today",
    )


def main():
    connector = GA4Connector(property_id=PROPERTY_ID)

    print("\nExample 1: Active users by country")
    country_report = active_users_by_country(connector)
    print(country_report)

    print("\nExample 2: Event counts by event name")
    event_report = event_counts_by_event_name(connector)
    print(event_report)


if __name__ == "__main__":
    main()