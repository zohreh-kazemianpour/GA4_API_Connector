from dataclasses import dataclass

import pandas as pd

from .connector import GA4Connector


@dataclass
class GA4ReportConfig:
    property_id: str
    start_date: str
    end_date: str
    limit: int = 5000


class GA4Reporter:
    """GA4 report methods, can be extended to include more report types as needed."""

    def __init__(self, config: GA4ReportConfig):
        self.config = config
        self.connector = GA4Connector(property_id=config.property_id)

    def daily_activity(self) -> pd.DataFrame:
        return self.connector.run_report(
            dimensions=["date"],
            metrics=["activeUsers", "eventCount"],
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            limit=self.config.limit,
        )

    def active_users_by_country(self) -> pd.DataFrame:
        return self.connector.run_report(
            dimensions=["country", "city"],
            metrics=["activeUsers"],
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            limit=self.config.limit,
        )

    def event_counts_by_event_name(self) -> pd.DataFrame:
        return self.connector.run_report(
            dimensions=["eventName"],
            metrics=["eventCount"],
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            limit=self.config.limit,
        )