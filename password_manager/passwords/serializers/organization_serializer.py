from rest_framework import serializers
from ..models.organization_model import OrganizationModel, OrganizationPasswordsModel


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationModel
        fields = "__all__"


class OrganizationPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationPasswordsModel
        fields = "__all__"

