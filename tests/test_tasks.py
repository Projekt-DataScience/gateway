import requests

def test_tasks_reachable():
    r = requests.get('http://localhost/api/tasks/healthcheck')
    assert r.status_code == 200