from types import SimpleNamespace

import pandas as pd
import pytest

from ga4_connector.connector import GA4Connector


class FakeGA4Client:
    """Fake GA4 client so tests do not call the real Google API."""

    def __init__(self):
        self.request = None

    def run_report(self, request):
        self.request = request

        return SimpleNamespace(
            dimension_headers=[
                SimpleNamespace(name="country"),
            ],
            metric_headers=[
                SimpleNamespace(name="activeUsers"),
            ],
            rows=[
                SimpleNamespace(
                    dimension_values=[
                        SimpleNamespace(value="United Kingdom"),
                    ],
                    metric_values=[
                        SimpleNamespace(value="2"),
                    ],
                ),
                SimpleNamespace(
                    dimension_values=[
                        SimpleNamespace(value="United States"),
                    ],
                    metric_values=[
                        SimpleNamespace(value="1"),
                    ],
                ),
            ],
        )


def make_connector(fake_client):
    """Create GA4Connector without creating the real Google client."""
    connector = GA4Connector.__new__(GA4Connector)
    connector.property_id = "543114448"
    connector.client = fake_client
    return connector


def test_run_report_returns_dataframe():
    fake_client = FakeGA4Client()
    connector = make_connector(fake_client)

    result = connector.run_report(
        dimensions=["country"],
        metrics=["activeUsers"],
        start_date="today",
        end_date="today",
    )

    assert isinstance(result, pd.DataFrame)


def test_run_report_parses_ga4_response():
    fake_client = FakeGA4Client()
    connector = make_connector(fake_client)

    result = connector.run_report(
        dimensions=["country"],
        metrics=["activeUsers"],
        start_date="today",
        end_date="today",
    )

    assert list(result.columns) == ["country", "activeUsers"]
    assert len(result) == 2
    assert result.iloc[0]["country"] == "United Kingdom"
    assert result.iloc[0]["activeUsers"] == "2"
    assert result.iloc[1]["country"] == "United States"
    assert result.iloc[1]["activeUsers"] == "1"


def test_run_report_uses_property_id_in_request():
    fake_client = FakeGA4Client()
    connector = make_connector(fake_client)

    connector.run_report(
        dimensions=["country"],
        metrics=["activeUsers"],
        start_date="today",
        end_date="today",
    )

    assert fake_client.request.property == "properties/543114448"


def test_run_report_rejects_empty_dimensions():
    fake_client = FakeGA4Client()
    connector = make_connector(fake_client)

    with pytest.raises(ValueError, match="At least one dimension"):
        connector.run_report(
            dimensions=[],
            metrics=["activeUsers"],
            start_date="today",
            end_date="today",
        )


def test_run_report_rejects_empty_metrics():
    fake_client = FakeGA4Client()
    connector = make_connector(fake_client)

    with pytest.raises(ValueError, match="At least one metric"):
        connector.run_report(
            dimensions=["country"],
            metrics=[],
            start_date="today",
            end_date="today",
        )
