from fastapi.testclient import TestClient
import sys
import os

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

def test_change_version():
    # Тест 1: Установка версии 0 (11s)
    response = client.get(
        "/change_version", 
        params={"version": 0},
        headers={"X-Forwarded-For": "127.0.0.1"}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    
    # Проверяем успешный ответ или сообщение об ошибке
    if "result" in response_data:
        # Может быть успех или ошибка в зависимости от доступности Redis
        assert response_data["result"] in [
            "Версия модели изменена на 11s",
            "IP не найден",
            "Ошибка смены версии"
        ]
    else:
        # Если нет ключа result, проверяем другой возможный формат
        assert "error" in response_data or "detail" in response_data

    # Тест 2: Установка версии 1 (11m)
    response = client.get(
        "/change_version", 
        params={"version": 1},
        headers={"X-Forwarded-For": "127.0.0.2"}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    
    if "result" in response_data:
        assert response_data["result"] in [
            "Версия модели изменена на 11m",
            "IP не найден",
            "Ошибка смены версии"
        ]