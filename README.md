# GA4 API Connector

A lightweight Python project for retrieving Google Analytics 4 (GA4) data using the Google Analytics Data API.

The main deliverable is a reusable `GA4Connector` class that accepts a GA4 property ID, dimensions, metrics, and a date range, then calls the GA4 `runReport` API and returns the results as a pandas DataFrame.

The project also includes a small `GA4Reporter` helper layer for predefined example reports.

## Project Structure

```text
GA4_API_Connector/
├── ga4_connector/
│   ├── __init__.py
│   ├── connector.py
│   └── reporter.py
├── examples/
│   └── example_reports.py
├── tests/
│   └── test_connector.py
├── pyproject.toml
├── poetry.lock
├── .gitignore
└── README.md
```

## Setup

### 1. Install dependencies

This project uses Poetry.

From the project root, run:

```bash
poetry install --no-root
```

The main dependencies are:

```text
google-analytics-data
google-api-core
google-auth
pandas
openpyxl
pytest
```

### 2. Google Cloud and GA4 setup

Before running the connector, make sure you have:

1. A Google Cloud project.
2. The Google Analytics Data API enabled.
3. A service account with a downloaded JSON key.
4. The service-account email added as a Viewer on the GA4 property.
5. The numeric GA4 Property ID.

Use the numeric GA4 Property ID, for example:

```text
543114448
```

Do not use the GA4 Measurement ID, for example:

```text
G-XXXXXXXXXX
```

The Measurement ID is used by a website or app to send data into GA4. The numeric Property ID is used by the GA4 Data API to read report data.

### 3. Authentication

Store the service-account JSON key safely and do not commit it to Git.

Set the credentials path in your terminal before running examples:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/credentials/ga4-service-account.json"
```

The connector uses Google’s default authentication mechanism through the Google Analytics client library.

## Usage

The example file is located at:

```text
examples/example_reports.py
```

Update the property ID and date range in that file if needed:

```python
PROPERTY_ID = "543114448"
START_DATE = "30daysAgo"
END_DATE = "today"
```

Then run:

```bash
PYTHONPATH=. poetry run python -m examples.example_reports
```

The example script runs two reports:

1. Active users and event count by date.
2. Event counts by event name.

Example output:

```text
Example 1: Active users and event count by date
       date activeUsers eventCount
0  20260630           4         61
1  20260706           1          3

Example 2: Event counts by event name
          eventName eventCount
0     service_click         17
1         page_view         10
2  learn_more_click          8
3            scroll          8
4     session_start          6
5     contact_click          5
6   user_engagement          5
7       first_visit          4
8             click          1
```

A simple Netlify test website was used to generate GA4 events for validation.

## Core Connector

The main connector class is in:

```text
ga4_connector/connector.py
```

Example direct usage:

```python
from ga4_connector import GA4Connector

connector = GA4Connector(property_id="543114448")

report = connector.run_report(
    dimensions=["date"],
    metrics=["activeUsers", "eventCount"],
    start_date="30daysAgo",
    end_date="today",
)

print(report)
```

`GA4Connector.run_report()` accepts:

- `dimensions`: a list of GA4 dimension names
- `metrics`: a list of GA4 metric names
- `start_date`: report start date
- `end_date`: report end date
- `limit`: optional row limit, defaulting to `5000`

It returns a pandas DataFrame.

## Reporter Layer

The reporter helper is in:

```text
ga4_connector/reporter.py
```

It provides a small layer on top of `GA4Connector` for predefined report methods.

Current report methods include:

- `daily_activity()`
- `active_users_by_country()`
- `event_counts_by_event_name()`

Example:

```python
from ga4_connector import GA4ReportConfig, GA4Reporter

config = GA4ReportConfig(
    property_id="543114448",
    start_date="30daysAgo",
    end_date="today",
)

reporter = GA4Reporter(config)

print(reporter.daily_activity())
print(reporter.event_counts_by_event_name())
```

## Running Tests

Run the automated tests with:

```bash
PYTHONPATH=. poetry run pytest
```

The tests use a fake GA4 client, so they do not require live Google credentials or API access.

The tests check that `GA4Connector.run_report()`:

- returns a pandas DataFrame
- parses GA4-style API responses correctly
- uses the correct property ID in the request
- rejects empty dimensions
- rejects empty metrics

## Error Handling

`GA4Connector` includes basic error handling for:

- missing dimensions
- missing metrics
- authentication failures
- permission errors
- invalid GA4 requests
- general Google API errors

Common causes of errors include:

- using the GA4 Measurement ID instead of the numeric Property ID
- not adding the service-account email as a Viewer on the GA4 property
- using invalid dimension or metric names
- not setting `GOOGLE_APPLICATION_CREDENTIALS`

## Security Notes

Do not commit credentials or generated local files.

The `.gitignore` includes:

```text
credentials/
*.json
.env
.venv/
__pycache__/
*.py[cod]
*.xlsx
```

Service-account keys should stay local and should be supplied through an environment variable such as `GOOGLE_APPLICATION_CREDENTIALS`.

## Notes

GA4 Realtime reports and GA4 Data API reports may not always match immediately. Realtime data can appear quickly in the GA4 interface, while processed report data available through the Data API can take longer.

Large date ranges or high-cardinality dimensions may also affect returned results due to GA4 reporting behaviour such as thresholding or sampling.