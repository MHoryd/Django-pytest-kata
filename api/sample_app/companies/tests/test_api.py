from django.test import Client
from django.urls import reverse
from api.sample_app.companies.models import Company
import pytest
import json


client = Client()
companies_url = reverse("companies-list")

pytestmark = pytest.mark.django_db

# Test get companies


def test_zero_companies_should_return_empty_list() -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succeed() -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    parsed = json.loads(response.content)
    assert response.status_code == 200
    assert parsed[0]["name"] == test_company.name
    assert parsed[0]["status"] == "Hiring"
    assert parsed[0]["application_link"] == ""
    assert parsed[0]["notes"] == ""
    test_company.delete()


# Test post companies


def test_create_company_without_arguments_should_fail() -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_company_with_duplicated_name_should_fail() -> None:
    Company.objects.create(name="Amazon")
    response = client.post(path=companies_url, data={"name": "Amazon"})
    parsed = json.loads(response.content)
    assert response.status_code == 400
    assert parsed["name"] == ["company with this name already exists."]


def test_create_company_with_only_name_should_be_default() -> None:
    response = client.post(path=companies_url, data={"name": "Amazon"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "Amazon"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_status_layoffs_should_succeed() -> None:
    response = client.post(
        path=companies_url, data={"name": "Amazon", "status": "Layoffs"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "Amazon"
    assert response_content.get("status") == "Layoffs"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_wrong_status_should_succeed() -> None:
    response = client.post(path=companies_url, data={"name": "Amazon", "status": "xyz"})
    assert response.status_code == 400
    response_content = json.loads(response.content)
    assert "xyz" in str(response_content)
    assert "is not a valid choice." in response_content.get("status")[0]