import pandas as pd

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.api_core.exceptions import GoogleAPIError, InvalidArgument, PermissionDenied, Unauthenticated



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
        limit: int = 5000,
    ) -> pd.DataFrame:

        if not dimensions:
            raise ValueError("At least one dimension must be provided.")

        if not metrics:
            raise ValueError("At least one metric must be provided.")

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            limit=limit,
        )

        try:
            response = self.client.run_report(request)

        except Unauthenticated as exc:
            raise RuntimeError(
                "Authentication failed. Check your service-account credentials."
            ) from exc

        except PermissionDenied as exc:
            raise RuntimeError(
                "Permission denied. Ensure the service account has Viewer access to the GA4 property."
            ) from exc

        except InvalidArgument as exc:
            raise ValueError(
                "Invalid request. Check the property ID, dimensions, metrics, and date range."
            ) from exc

        except GoogleAPIError as exc:
            raise RuntimeError(
                f"Google Analytics API error: {exc}"
            ) from exc

        rows = []
        for row in response.rows:
            record = {}

            for header, value in zip(response.dimension_headers, row.dimension_values):
                record[header.name] = value.value

            for header, value in zip(response.metric_headers, row.metric_values):
                record[header.name] = value.value

            rows.append(record)

        return pd.DataFrame(rows)