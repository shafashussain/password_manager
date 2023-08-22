from django.db import models
from .common_info_model import CommonInfoModel
from .organization_model import OrganizationModel
from password_manager.validators.password_validator import password_validator


class UserModel(CommonInfoModel):
    """
    A table to store the users basic informations
    """
    username = models.CharField(max_length=100, null=True, unique=True)
    email_id = models.EmailField(blank=True, null=True)
    mobile_number = models.PositiveBigIntegerField(unique=True, null=True)
    organization = models.ForeignKey(OrganizationModel, on_delete=models.SET_NULL, null=True)
    is_admin = models.BooleanField(default=True)

    class Meta:
        db_table = "UserModel"
        ordering = ['-created_at']


class UserLoginModel(CommonInfoModel):
    """
    A place holder table to store the user credentials
    """
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    password = models.CharField(max_length=100, validators =[password_validator])
    last_password_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UserLogin"
        ordering = ['-created_at']

