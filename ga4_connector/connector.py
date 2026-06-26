from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest


class GA4Connector:
    """Connector for the Google Analytics 4 Data API."""

    def __init__(self, property_id: str):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()
    


    def run_report(
        self,
        dimensions: list[str],
        metrics: list[str],
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )

        response = self.client.run_report(request)

        results = []

        for row in response.rows:
            record = {}

            for header, value in zip(response.dimension_headers, row.dimension_values):
                record[header.name] = value.value

            for header, value in zip(response.metric_headers, row.metric_values):
                record[header.name] = value.value

            results.append(record)

        return results