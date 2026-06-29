# reporter.py

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .connector import GA4Connector


# Currently, using mock data, but once acess is granted, will adjust.
# Ensured that the calls were not too expensive.
@dataclass
class GA4ReportConfig:
    property_id: str
    start_date: str
    end_date: str
    output_path: str = "mcs_ws_ga4_report.xlsx"


class GA4Reporter:
    """Builds GA4 reporting outputs for M&C Saatchi WS."""

    def __init__(self, config: GA4ReportConfig):
        self.config = config
        self.connector = GA4Connector(property_id=config.property_id)

    def daily_overview(self) -> pd.DataFrame:
        return self.connector.run_report(
            dimensions=["date"],
            metrics=[
                "activeUsers",
                "sessions",
                "engagedSessions",
                "engagementRate",
                "conversions",
                "totalRevenue",
            ],
            start_date=self.config.start_date,
            end_date=self.config.end_date,
        )

    def page_channel_report(self) -> pd.DataFrame:
        return self.connector.run_report(
            dimensions=[
                "sessionDefaultChannelGroup",
                "landingPagePlusQueryString",
            ],
            metrics=[
                "sessions",
                "activeUsers",
                "engagedSessions",
                "conversions",
                "totalRevenue",
            ],
            start_date=self.config.start_date,
            end_date=self.config.end_date,
        )

    def product_report(self) -> pd.DataFrame:
        return self.connector.run_report(
            dimensions=["itemName"],
            metrics=[
                "itemsViewed",
                "itemsAddedToCart",
                "itemsPurchased",
                "itemRevenue",
            ],
            start_date=self.config.start_date,
            end_date=self.config.end_date,
        )

    def event_report(self) -> pd.DataFrame:
        return self.connector.run_report(
            dimensions=["eventName"],
            metrics=[
                "eventCount",
                "activeUsers",
                "conversions",
                "totalRevenue",
            ],
            start_date=self.config.start_date,
            end_date=self.config.end_date,
        )

    def _to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        dimension_columns = {
            "date",
            "sessionDefaultChannelGroup",
            "landingPagePlusQueryString",
            "itemName",
            "eventName",
        }

        for column in df.columns:
            if column not in dimension_columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")

        return df

    def build_channel_summary(self, page_channel_df: pd.DataFrame) -> pd.DataFrame:
        page_channel_df = self._to_numeric(page_channel_df)

        return (
            page_channel_df
            .groupby("sessionDefaultChannelGroup", as_index=False)
            .agg({
                "sessions": "sum",
                "activeUsers": "sum",
                "engagedSessions": "sum",
                "conversions": "sum",
                "totalRevenue": "sum",
            })
            .sort_values("sessions", ascending=False)
        )

    def build_landing_page_summary(self, page_channel_df: pd.DataFrame) -> pd.DataFrame:
        page_channel_df = self._to_numeric(page_channel_df)

        return (
            page_channel_df
            .groupby("landingPagePlusQueryString", as_index=False)
            .agg({
                "sessions": "sum",
                "activeUsers": "sum",
                "engagedSessions": "sum",
                "conversions": "sum",
                "totalRevenue": "sum",
            })
            .sort_values("sessions", ascending=False)
        )

    def build_findings(self, data: dict[str, pd.DataFrame]) -> pd.DataFrame:
        overview = self._to_numeric(data["Daily Overview"])
        channel_summary = self._to_numeric(data["Channel Summary"])
        landing_page_summary = self._to_numeric(data["Landing Page Summary"])
        products = self._to_numeric(data["Products"])

        findings = []

        total_users = overview["activeUsers"].sum()
        total_sessions = overview["sessions"].sum()
        total_revenue = overview["totalRevenue"].sum()

        findings.append({
            "Theme": "Executive summary",
            "Finding": f"The site generated {total_users:,.0f} active users and {total_sessions:,.0f} sessions.",
            "Implication": "This provides the baseline for website demand and audience quality.",
            "Recommended action": "Compare performance against the previous period and review channel-level drivers.",
        })

        findings.append({
            "Theme": "Revenue",
            "Finding": f"Total reported revenue was {total_revenue:,.2f}.",
            "Implication": "Revenue should be analysed by channel, landing page, and product.",
            "Recommended action": "Prioritise the journeys that drive the highest revenue per session.",
        })

        if not channel_summary.empty:
            top_channel = channel_summary.iloc[0]

            findings.append({
                "Theme": "Acquisition",
                "Finding": f"{top_channel['sessionDefaultChannelGroup']} was the largest channel by sessions.",
                "Implication": "This channel is the main traffic driver.",
                "Recommended action": "Check whether it also drives efficient conversions and revenue.",
            })

        if not landing_page_summary.empty:
            top_page = landing_page_summary.iloc[0]

            findings.append({
                "Theme": "Landing pages",
                "Finding": f"The top landing page was {top_page['landingPagePlusQueryString']}.",
                "Implication": "This page has high influence over first impressions and conversion journeys.",
                "Recommended action": "Audit messaging, CTAs, page speed, and product discovery.",
            })

        if not products.empty:
            top_product = products.sort_values("itemRevenue", ascending=False).iloc[0]

            findings.append({
                "Theme": "Ecommerce",
                "Finding": f"The highest-revenue product was {top_product['itemName']}.",
                "Implication": "Revenue may be concentrated around a small number of hero products.",
                "Recommended action": "Use this insight for merchandising, paid media, and cross-sell planning.",
            })

        return pd.DataFrame(findings)

    def export(self) -> Path:
        daily_overview = self.daily_overview()
        page_channel = self.page_channel_report()
        products = self.product_report()
        events = self.event_report()

        channel_summary = self.build_channel_summary(page_channel)
        landing_page_summary = self.build_landing_page_summary(page_channel)

        data = {
            "Daily Overview": daily_overview,
            "Page Channel": page_channel,
            "Channel Summary": channel_summary,
            "Landing Page Summary": landing_page_summary,
            "Products": products,
            "Events": events,
        }

        data["Findings"] = self.build_findings(data)

        output_path = Path(self.config.output_path)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for sheet_name, df in data.items():
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

        return output_path