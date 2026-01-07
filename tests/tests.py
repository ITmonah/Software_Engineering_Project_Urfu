from fastapi.testclient import TestClient
import sys
import os

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

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
          "name": "cat"
        }
    ]
}
    
    response = client.get("/detect", params={"image_url": "https://i.ytimg.com/vi/jg8ixdQzrjc/maxresdefault.jpg"})
    assert response.status_code == 200
    actual_result = response.json()
    
    # Сравниваем количество обнаруженных объектов
    assert len(actual_result["results"]) == len(expected_result["results"])
    
    # Сравниваем каждый объект по отдельности
    for i, expected_obj in enumerate(expected_result["results"]):
        actual_obj = actual_result["results"][i]
        
        # Для координат и уверенности используем приблизительное сравнение (+- 5 пикселей)
        assert actual_obj["name"] == expected_obj["name"]
        assert actual_obj["class_"] == expected_obj["class_"]
        assert abs(actual_obj["xmin"] - expected_obj["xmin"]) < 5.0
        assert abs(actual_obj["ymin"] - expected_obj["ymin"]) < 5.0
        assert abs(actual_obj["xmax"] - expected_obj["xmax"]) < 5.0
        assert abs(actual_obj["ymax"] - expected_obj["ymax"]) < 5.0
        assert abs(actual_obj["confidence"] - expected_obj["confidence"]) < 0.1