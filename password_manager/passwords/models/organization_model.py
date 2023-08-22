import uuid
from django.db import models
from .common_info_model import CommonInfoModel
from password_manager.validators.password_validator import password_validator


class OrganizationModel(CommonInfoModel):
    """
    Place holder table to hold organization details
    """

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, default="")

    class Meta:
        db_table = "Organization"
        ordering = ['-created_at']


class OrganizationPasswordsModel(CommonInfoModel):
    """
    A place holder table to store the organization credentials
    """
    organization = models.OneToOneField(OrganizationModel, on_delete=models.CASCADE)
    password = models.CharField(max_length=100, validators =[password_validator])
    last_password_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "OrganizationPasswords"
        ordering = ['-created_at']
