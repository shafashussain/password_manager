from rest_framework.views import APIView

from passwords.models.organization_model import OrganizationModel
from passwords.serializers.organization_serializer import OrganizationSerializer

from password_manager.responses.response_handling import ResponseHandling


class OrganizationsView(APIView):
    @staticmethod
    def post(request):
        try:
            payload = request.data.dict()

            organizations = OrganizationSerializer(data=payload)
            if organizations.is_valid():
                organizations.save()
                return ResponseHandling.create_success(organizations.data)

            return ResponseHandling.bad_request(organizations.errors)

        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ----------------------------------------------------------------

    @staticmethod
    def get(request):
        """
        Used to fetch organizations
        """
        try:
            payload = request.GET.dict()

            organizations = OrganizationModel.objects.filter(**payload)
            serializer = OrganizationSerializer(organizations, many=True)

            if len(serializer.data):
                return ResponseHandling.retrieve_list_success(
                    serializer.data,
                )
            else:
                return ResponseHandling.no_records()

        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ----------------------------------------------------------------

    @classmethod
    def patch(self, request):
        """
        Used to update organization
        """
        try:
            payload = request.POST.dict()
            if "primary_key" in payload:
                get_data = OrganizationModel.objects.get(
                    primary_key=payload["primary_key"]
                )
                serializer = OrganizationSerializer(get_data, data=payload, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return ResponseHandling.query_success("Organization is Updated Successfully")
                return ResponseHandling.bad_request(serializer.errors)
            else:
                return ResponseHandling.input_format_error("Primary key is mandatory field")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ------------------------------------------------------------------------------------

    @staticmethod
    def delete(request):
        """
        Used to delete organization
        """
        try:
            payload = request.data.dict()
            if "primary_key" in payload:
                get_data = OrganizationModel.objects.get(
                    primary_key=payload["primary_key"]
                )
                get_data.delete()
                return ResponseHandling.query_success("Organization is Deleted Successfully")
            else:
                return ResponseHandling.input_format_error("Primary key is mandatory field")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))
