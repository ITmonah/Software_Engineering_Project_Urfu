from fastapi.testclient import TestClient
import sys
import os

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_detect_valid_image():
    response = client.get("/detect", params={"image_url": "https://ultralytics.com/images/zidane.jpg"})
    assert response.status_code == 200