import pytest
URL = '/resend'


@pytest.mark.github
@pytest.mark.local
@pytest.mark.server
def test_aiohttp_route_ok(tclient, base_url, payload_aiohttp):
    response = tclient.post(base_url + URL, json=payload_aiohttp)
    assert response.status_code == 200
    data: dict = response.json()
    assert data['message'] == ''
    assert data['errors'] == []
    assert data['data']
    assert data['result']


@pytest.mark.github
@pytest.mark.local
@pytest.mark.server
def test_aiohttp_route_bad_url(tclient, base_url, payload_aiohttp):
    payload_aiohttp['request_data']['url'] = 'blable'
    response = tclient.post(base_url + URL, json=payload_aiohttp)
    assert response.status_code == 200
    data: dict = response.json()
    assert data['message'].startswith('Invalid url')
    assert data['errors'] == []
    assert data['result'] is False


@pytest.mark.github
@pytest.mark.local
@pytest.mark.server
def test_requests_route_ok(tclient, base_url, payload_requests):
    response = tclient.post(base_url + URL, json=payload_requests)
    assert response.status_code == 200
    data: dict = response.json()
    assert data['message'] == ''
    assert data['errors'] == []
    assert data['data']
    assert data['result']


@pytest.mark.github
@pytest.mark.local
@pytest.mark.server
def test_requests_route_bad_url(tclient, base_url, payload_requests):
    payload_requests['request_data']['url'] = 'blable'
    response = tclient.post(base_url + URL, json=payload_requests)
    assert response.status_code == 200
    data: dict = response.json()
    assert data['message'].startswith('Invalid url')
    assert data['errors'] == []
    assert data['result'] is False
