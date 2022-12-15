import requests

def test_audit_reachable():
    r = requests.get('http://localhost/api/audit/healthcheck')
    assert r.status_code == 200
