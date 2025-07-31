from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .serializer import CompanySerializer
from .models import Company
import requests
import os


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("last_update")


@api_view(http_method_names=["POST"])
def send_company_email(request: Request) -> Response:
    """Method to sed email via mailgun provider. Must provide"""
    response = requests.post(
        url=str(os.getenv("MAILGUN_ENDPOINT")),
        auth=("api", str(os.getenv("MAILGUN_API_KEY"))),
        data={
            "from": f"Mailgun Sandbox <{os.getenv('MAILGUN_SENDER_EMAIL')}>",
            "to": f"<{os.getenv('MAINGUN_RECEIVER_EMAIL')}>",
            "subject": str(request.data.get("subject")),
            "text": str(request.data.get("message")),
        },
    )
    if response.status_code == 200:
        return Response(
            {"status": "success", "info": "email send successfully"}, status=200
        )
    else:
        return Response(
            {"status": "failure", "info": "email not send successfully"}, status=400
        )
