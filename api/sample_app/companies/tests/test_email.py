import json
from unittest.mock import patch


@patch("api.sample_app.companies.views.requests.post")
def test_proper_response_on_success(mock_post, client) -> None:
    mock_post.return_value.status_code = 200

    payload = {"subject": "Test", "message": "Hello"}
    response = client.post("/send-email", data=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "success", "info": "email send successfully"}


@patch("api.sample_app.companies.views.requests.post")
def test_proper_response_on_failure(mock_post, client) -> None:
    mock_post.return_value.status_code = 400

    payload = {"subject": "Test", "message": "Hello"}
    response = client.post("/send-email", data=payload)

    assert response.status_code == 400
    assert response.json() == {
        "status": "failure",
        "info": "email not send successfully",
    }


def test_get_method_should_fail(client) -> None:
    response = client.get("/send-email")
    assert response.status_code == 405
    assert json.loads(response.content) == {"detail": 'Method "GET" not allowed.'}
