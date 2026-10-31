import hashlib
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingest.load_faers import flatten_event, quarter_date_range
from ingest.load_synthea import CONDITIONS_COLS, load_csv
from ingest.snowflake_utils import add_metadata


def test_quarter_date_range_supports_both_supported_formats():
    assert quarter_date_range("2024q4") == ("20241001", "20241231")
    assert quarter_date_range("24q4") == ("20241001", "20241231")
    assert quarter_date_range("2024q1") == ("20240101", "20240331")


def test_flatten_event_maps_expected_fields_and_uses_nulls_for_missing_values():
    event = {
        "safetyreportid": "1001",
        "safetyreportversion": "2",
        "transmissiondate": "20241231",
        "receivedate": "20250102",
        "reporttype": "1",
        "companynumb": "CMP-123",
        "patient": {
            "patientonsetage": "42",
            "patientonsetageunit": "801",
            "patientsex": "1",
            "patientweight": "80",
            "patientweightunit": "kg",
        },
        "primarysource": {
            "qualification": "1",
            "reportercountry": "US",
        },
        "sender": {"senderorganization": "ACME"},
        "occurcountry": "CA",
    }

    result = flatten_event(event)

    assert result["primaryid"] == "1001"
    assert result["caseversion"] == "2"
    assert result["mfr_dt"] == "20241231"
    assert result["fda_dt"] == "20250102"
    assert result["rept_cod"] == "1"
    assert result["mfr_num"] == "CMP-123"
    assert result["mfr_sndr"] == "ACME"
    assert result["age"] == "42"
    assert result["age_cod"] == "801"
    assert result["sex"] == "1"
    assert result["wt"] == "80"
    assert result["wt_cod"] == "kg"
    assert result["occp_cod"] == "1"
    assert result["reporter_country"] == "US"
    assert result["occr_country"] == "CA"
    assert result["caseid"] is None
    assert result["i_f_cod"] is None
    assert result["event_dt"] is None
    assert result["init_fda_dt"] is None
    assert result["age_grp"] is None
    assert result["to_mfr"] is None


def test_add_metadata_appends_standard_metadata_and_stable_hashes():
    df = pd.DataFrame({"record_id": ["A-1", "A-2"], "sex": ["M", "F"]})

    result = add_metadata(df, "demo.csv")

    assert {"_loaded_at", "_source_file", "_row_hash"}.issubset(result.columns)
    assert result["_source_file"].tolist() == ["demo.csv", "demo.csv"]
    assert result["_row_hash"].tolist() == [
        hashlib.md5("A-1|M".encode()).hexdigest(),
        hashlib.md5("A-2|F".encode()).hexdigest(),
    ]


def test_load_csv_renames_reserved_words_and_reindexes_columns(tmp_path, monkeypatch):
    csv_path = tmp_path / "conditions.csv"
    df = pd.DataFrame(
        {
            "start": ["2024-01-01", "2024-02-02"],
            "stop": ["2024-01-10", None],
            "patient": ["p1", "p2"],
            "encounter": ["e1", "e2"],
            "code": ["A1", "A2"],
            "system": ["sys", "sys"],
            "description": ["cond 1", "cond 2"],
        }
    )
    df.to_csv(csv_path, index=False)

    captured = {}

    def fake_load_to_snowflake(conn, framed_df, table_name):
        captured["table_name"] = table_name
        captured["columns"] = list(framed_df.columns)
        captured["row_count"] = len(framed_df)
        return len(framed_df)

    monkeypatch.setattr("ingest.load_synthea.load_to_snowflake", fake_load_to_snowflake)

    result = load_csv(csv_path, CONDITIONS_COLS, "SYNTHEA_CONDITIONS", object())

    assert result == 2
    assert captured["table_name"] == "SYNTHEA_CONDITIONS"
    assert captured["row_count"] == 2
    assert captured["columns"] == CONDITIONS_COLS + ["_loaded_at", "_source_file", "_row_hash"]
    assert "start_dt" in captured["columns"]
    assert "stop_dt" in captured["columns"]
    assert "start" not in captured["columns"]
    assert "stop" not in captured["columns"]


def test_fetch_faers_uses_a_stable_sort_and_handles_empty_results(monkeypatch):
    from ingest import load_faers

    calls = []

    class DummyResponse:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return {"results": []}

    def fake_send(self, prepared, timeout):
        calls.append(prepared.url)
        return DummyResponse()

    monkeypatch.setattr(load_faers.requests.Session, "send", fake_send)

    result = load_faers.fetch_faers("2024q4", 10)

    assert result.empty
    assert any("sort=safetyreportid:asc" in url for url in calls)
    assert any("skip=0" in url for url in calls)
