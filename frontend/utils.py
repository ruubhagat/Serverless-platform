# utils.py
import requests

BASE_URL = "http://localhost:8000/functions"

def list_functions():
    response = requests.get(BASE_URL)
    return response.json() if response.status_code == 200 else []

def create_function(data):
    return requests.post(BASE_URL, json=data)

def update_function(func_id, data):
    return requests.put(f"{BASE_URL}/{func_id}", json=data)

def delete_function(func_id):
    return requests.delete(f"{BASE_URL}/{func_id}")

def execute_function(func_id, runtime="runc"):
    return requests.post(f"{BASE_URL}/{func_id}/execute", params={"runtime": runtime})

def warmup_function(func_id, runtime="runc"):
    return requests.post(f"{BASE_URL}/{func_id}/warmup", params={"runtime": runtime})

def compare_performance(func_id, timeout=5.0):
    return requests.post(f"{BASE_URL}/compare-performance/", params={"func_id": func_id, "timeout": timeout})

def build_image(function_dir, image_name="gvisor-function-image"):
    return requests.post(f"{BASE_URL}/build-image/", json={"function_dir": function_dir, "image_name": image_name})

def get_metrics():
    return requests.get(f"{BASE_URL}/metrics")
