from django.contrib import admin
from api.sample_app.companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
