from ga4_connector.connector import GA4Connector

# Temporary property for testing
PROPERTY_ID = "543114448"


def main():
    connector = GA4Connector(property_id=PROPERTY_ID)

    results = connector.run_report(
        dimensions=["country"],
        metrics=["activeUsers"],
        start_date="7daysAgo",
        end_date="today",
    )

    print(results)


if __name__ == "__main__":
    main()