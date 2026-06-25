from google.analytics.data_v1beta import BetaAnalyticsDataClient


class GA4Connector:
    """Connector for the Google Analytics 4 Data API."""

    def __init__(self, property_id: str):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()