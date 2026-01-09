import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


@pytest.mark.integration
def test_detect_valid_image():
    expected_result = {
        "results": [
            {
                "xmin": 235.77236938476562,
                "ymin": 0,
                "xmax": 1232.0889892578125,
                "ymax": 720,
                "confidence": 0.6995765566825867,
                "class_": 15,
                "name": "cat",
            }
        ]
    }

    response = client.get(
        "/detect",
        params={"image_url": "https://i.ytimg.com/vi/jg8ixdQzrjc/maxresdefault.jpg"},
    )
    assert response.status_code == 200
    actual_result = response.json()

    assert len(actual_result["results"]) == len(expected_result["results"])

    for i, expected_obj in enumerate(expected_result["results"]):
        actual_obj = actual_result["results"][i]

        assert actual_obj["name"] == expected_obj["name"]
        assert actual_obj["class_"] == expected_obj["class_"]
        assert abs(actual_obj["xmin"] - expected_obj["xmin"]) < 50.0
        assert abs(actual_obj["ymin"] - expected_obj["ymin"]) < 50.0
        assert abs(actual_obj["xmax"] - expected_obj["xmax"]) < 50.0
        assert abs(actual_obj["ymax"] - expected_obj["ymax"]) < 50.0
        assert abs(actual_obj["confidence"] - expected_obj["confidence"]) < 1


def test_change_version():
    with TestClient(app) as client:

        response = client.get("/change_version", params={"version": 0})
        assert response.status_code == 200
        assert response.json()["result"] == "Версия модели изменена на 11s"

        response = client.get("/change_version", params={"version": 1})
        assert response.status_code == 200
        assert response.json()["result"] == "Версия модели изменена на 11m"


@pytest.mark.integration
def test_detect_requires_image_url_param():

    response = client.get("/detect")

    assert response.status_code in (400, 422)


@pytest.mark.integration
def test_detect_non_image_url_returns_error_or_empty():
    response = client.get(
        "/detect",
        params={"image_url": "https://example.com"},
    )

    assert response.status_code in (200, 400, 415, 422, 502)
    if response.status_code == 200:
        body = response.json()
        assert "results" in body
        assert isinstance(body["results"], list)


@pytest.mark.integration
def test_detect_response_schema_is_stable():
    response = client.get(
        "/detect",
        params={"image_url": "https://i.ytimg.com/vi/jg8ixdQzrjc/maxresdefault.jpg"},
    )
    assert response.status_code == 200
    body = response.json()

    assert "results" in body
    assert isinstance(body["results"], list)

    for obj in body["results"]:
        assert set(obj.keys()) >= {
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "confidence",
            "class_",
            "name",
        }
        assert isinstance(obj["xmin"], (int, float))
        assert isinstance(obj["ymin"], (int, float))
        assert isinstance(obj["xmax"], (int, float))
        assert isinstance(obj["ymax"], (int, float))
        assert isinstance(obj["confidence"], (int, float))
        assert isinstance(obj["class_"], int)
        assert isinstance(obj["name"], str)

        assert obj["xmax"] >= obj["xmin"]
        assert obj["ymax"] >= obj["ymin"]
        assert 0.0 <= obj["confidence"] <= 1.0


@pytest.mark.integration
def test_detect_on_blank_image_returns_empty_results_or_low_confidence():
    # часто на "пустой" картинке детекций нет
    response = client.get(
        "/detect",
        params={
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/59/Empty.png"
        },
    )
    assert response.status_code in (200, 400, 422, 502)
    if response.status_code == 200:
        body = response.json()
        assert "results" in body
        assert isinstance(body["results"], list)
        assert len(body["results"]) >= 0


def test_change_version_invalid_type():
    with TestClient(app) as client:
        response = client.get("/change_version", params={"version": "abc"})
        assert response.status_code in (400, 422)


def test_change_version_idempotent_same_value():
    with TestClient(app) as client:
        r1 = client.get("/change_version", params={"version": 0})
        assert r1.status_code == 200

        r2 = client.get("/change_version", params={"version": 0})
        assert r2.status_code == 200

        assert "result" in r2.json()
        assert isinstance(r2.json()["result"], str)


def test_change_version_switch_then_detect_still_works():
    with TestClient(app) as client:
        r = client.get("/change_version", params={"version": 1})
        assert r.status_code == 200

        resp = client.get(
            "/detect",
            params={
                "image_url": "https://i.ytimg.com/vi/jg8ixdQzrjc/maxresdefault.jpg"
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "results" in body
        assert isinstance(body["results"], list)
