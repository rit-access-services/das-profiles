from apistar.test import TestClient
import app


def test_get_all_profiles():
    """
    Testing the main view
    """
    client = TestClient()
    response = client.get('http://localhost/')
    assert response.status_code == 200


def test_refresh_profile_data():
    """
    Testing the function that updates profile data in the background
    """
    res = app.refresh_profile_data()
    assert res.status == 204
    app.BUCKET_NAME = 'somebucket-that-doesnt-exist'
    res = app.refresh_profile_data()
    assert res.status == 500
