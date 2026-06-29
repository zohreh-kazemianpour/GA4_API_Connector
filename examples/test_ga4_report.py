"""
Test runner for GA4Reporter without calling the real GA4 API.

How to use:
1. Place this file in the same folder as:
   - connector.py
   - reporter.py

2. Install dependencies if needed:
   pip install pandas openpyxl

3. Run:
   python test_ga4_report.py

Expected result:
- A file called test_mcs_ws_ga4_report.xlsx is created.
- The terminal prints the workbook path and sheet names.

This test replaces the real GA4Connector with a mock connector, so no GA4 credentials
or property access are required.
"""

from pathlib import Path

import pandas as pd

import reporter
from reporter import GA4ReportConfig, GA4Reporter


class MockGA4Connector:
    """Mock connector that returns fake GA4-style data for local testing."""

    def __init__(self, property_id: str):
        self.property_id = property_id

    def run_report(
        self,
        dimensions: list[str],
        metrics: list[str],
        start_date: str,
        end_date: str,
        limit: int = 10000,
    ) -> pd.DataFrame:
        if dimensions == ["date"]:
            return pd.DataFrame([
                {
                    "date": "20260601",
                    "activeUsers": "1200",
                    "sessions": "1500",
                    "engagedSessions": "900",
                    "engagementRate": "0.60",
                    "conversions": "75",
                    "totalRevenue": "8200.50",
                },
                {
                    "date": "20260602",
                    "activeUsers": "1350",
                    "sessions": "1700",
                    "engagedSessions": "1088",
                    "engagementRate": "0.64",
                    "conversions": "92",
                    "totalRevenue": "10450.75",
                },
            ])

        if dimensions == ["sessionDefaultChannelGroup", "landingPagePlusQueryString"]:
            return pd.DataFrame([
                {
                    "sessionDefaultChannelGroup": "Organic Search",
                    "landingPagePlusQueryString": "/",
                    "sessions": "1200",
                    "activeUsers": "980",
                    "engagedSessions": "780",
                    "conversions": "70",
                    "totalRevenue": "9000.00",
                },
                {
                    "sessionDefaultChannelGroup": "Paid Search",
                    "landingPagePlusQueryString": "/store.html",
                    "sessions": "900",
                    "activeUsers": "760",
                    "engagedSessions": "510",
                    "conversions": "55",
                    "totalRevenue": "7300.00",
                },
                {
                    "sessionDefaultChannelGroup": "Direct",
                    "landingPagePlusQueryString": "/basket.html",
                    "sessions": "400",
                    "activeUsers": "330",
                    "engagedSessions": "210",
                    "conversions": "42",
                    "totalRevenue": "2351.25",
                },
            ])

        if dimensions == ["itemName"]:
            return pd.DataFrame([
                {
                    "itemName": "Google T-Shirt",
                    "itemsViewed": "900",
                    "itemsAddedToCart": "180",
                    "itemsPurchased": "75",
                    "itemRevenue": "3750.00",
                },
                {
                    "itemName": "Google Hoodie",
                    "itemsViewed": "650",
                    "itemsAddedToCart": "145",
                    "itemsPurchased": "61",
                    "itemRevenue": "6100.00",
                },
            ])

        if dimensions == ["eventName"]:
            return pd.DataFrame([
                {
                    "eventName": "page_view",
                    "eventCount": "8500",
                    "activeUsers": "2500",
                    "conversions": "0",
                    "totalRevenue": "0",
                },
                {
                    "eventName": "add_to_cart",
                    "eventCount": "325",
                    "activeUsers": "280",
                    "conversions": "0",
                    "totalRevenue": "0",
                },
                {
                    "eventName": "purchase",
                    "eventCount": "167",
                    "activeUsers": "140",
                    "conversions": "167",
                    "totalRevenue": "18651.25",
                },
            ])

        raise ValueError(f"No mock data defined for dimensions: {dimensions}")


def main() -> None:
    # Replace the real connector used inside reporter.py with the mock connector.
    reporter.GA4Connector = MockGA4Connector

    config = GA4ReportConfig(
        property_id="mock-property-id",
        start_date="30daysAgo",
        end_date="yesterday",
        output_path="test_mcs_ws_ga4_report.xlsx",
    )

    ga4_reporter = GA4Reporter(config)
    output_path = ga4_reporter.export()

    if not Path(output_path).exists():
        raise FileNotFoundError(f"Report was not created: {output_path}")

    workbook = pd.ExcelFile(output_path)

    print("Report test passed.")
    print(f"Created workbook: {output_path}")
    print("Sheets:")
    for sheet in workbook.sheet_names:
        print(f"- {sheet}")


if __name__ == "__main__":
    main()
