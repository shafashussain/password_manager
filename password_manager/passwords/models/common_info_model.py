from django.db import models
import uuid


class CommonInfoModel(models.Model):
    """
    Common fields model
    Table to hold primary key and created time
    """
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
