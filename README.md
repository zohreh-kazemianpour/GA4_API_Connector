# GA4 API Connector

A lightweight Python package for retrieving Google Analytics 4 (GA4) data and generating reports. The project is designed to separate the GA4 API layer from the reporting layer, making it easy to extend for additional reports or integrate with other analytics workflows.

# Project Structure

GA4_API_Connector/
├── ga4_connector/
│   ├── __init__.py
│   ├── connector.py
│   └── reporter.py
├── examples/
│   ├── example_reports.py
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

Update the GA4 property ID and date range in examples/example_reports.py.
A mock website was created to test report generation.

Run:

PYTHONPATH=. poetry run python examples/example_reports.py

This extracts the data from the mock website, allowing the connector and reporting pipeline to be validated.

# Design

The project is organised into two main components:

GA4Connector (connector.py) – Handles communication with the Google Analytics Data API and returns results as pandas DataFrames.
examples_reports.py - Groups active users by coutries, and groups events by event name.