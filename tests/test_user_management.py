import requests

def test_user_management_reachable():
    r = requests.get('http://localhost/api/user_management/docs')
    assert r.status_code == 200