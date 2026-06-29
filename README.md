# GA4 API Connector

A lightweight Python package for retrieving Google Analytics 4 (GA4) data and generating Excel reports. The project is designed to separate the GA4 API layer from the reporting layer, making it easy to extend for additional reports or integrate with other analytics workflows.

# Project Structure

GA4_API_Connector/
├── ga4_connector/
│   ├── __init__.py
│   ├── connector.py
│   └── reporter.py
├── examples/
│   ├── example_reports.py
│   └── test_ga4_report.py
├── pyproject.toml
└── README.md

# Setup
1. Install dependencies

Using Poetry:

poetry install --no-root

If dependencies have not yet been added:

poetry add pandas openpyxl google-analytics-data google-api-core google-auth
2. Authentication

The current implementation assumes Google Cloud authentication has been configured (for example, using a service account). The connector uses the default Google authentication mechanism. Once production access is granted, the authentication configuration will be updated as required.

# Usage

Create a report configuration and generate the report:

from ga4_connector.reporter import GA4ReportConfig, GA4Reporter

config = GA4ReportConfig(
    property_id="YOUR_GA4_PROPERTY_ID",
    start_date="30daysAgo",
    end_date="yesterday",
    output_path="ga4_report.xlsx",
)

reporter = GA4Reporter(config)
reporter.export()

The generated workbook contains multiple worksheets, including:

Daily Overview
Page Channel
Channel Summary
Landing Page Summary
Products
Events
Findings
Testing

A mock-data example is included to test report generation without connecting to the GA4 API.

Run:

PYTHONPATH=. poetry run python examples/test_ga4_report.py

This creates a sample Excel report using mock GA4 data, allowing the reporting pipeline to be validated without requiring Google Analytics credentials.

# Design

The project is organised into two main components:

GA4Connector (connector.py) – Handles communication with the Google Analytics Data API and returns results as pandas DataFrames.
GA4Reporter (reporter.py) – Builds reports, aggregates metrics, generates business findings, and exports the results to Excel.

This separation allows the connector to be reused independently while keeping reporting logic modular and easy to extend.