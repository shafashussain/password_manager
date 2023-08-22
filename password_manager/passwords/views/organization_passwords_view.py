from rest_framework.views import APIView

from passwords.models.organization_model import OrganizationPasswordsModel, OrganizationModel
from passwords.models.user_model import UserModel
from passwords.serializers.organization_serializer import OrganizationPasswordSerializer

from password_manager.responses.response_handling import ResponseHandling


class OrganizationPasswordsView(APIView):

    @staticmethod
    def post(request):
        try:
            payload = request.data.dict()
            organization_passwords = OrganizationPasswordSerializer(data=payload)
            if organization_passwords.is_valid():
                organization_passwords.save()
                return ResponseHandling.create_success(organization_passwords.data)
            return ResponseHandling.bad_request(organization_passwords.errors)

        except Exception as e:
            return ResponseHandling.bad_request(str(e))
        
    # ------------------------------------------------------------------------------------

    @staticmethod
    def get(request):
        """
        Used to fetch organization passwords
        """
        try:
            payload = request.GET.dict()

            if "organization" in payload and "user" in payload:
                payload["organization"] = OrganizationModel.objects.get(
                    primary_key=payload["organization"]
                )
                queyset = UserModel.objects.filter(
                    primary_key=payload["user"],
                    organization=payload["organization"]
                )
                if len(queyset) > 0:
                    organization_passwords = OrganizationPasswordsModel.objects.filter(organization=payload["organization"])
                    serializer = OrganizationPasswordSerializer(organization_passwords, many=True)

                    if len(serializer.data):
                        return ResponseHandling.retrieve_list_success(
                            serializer.data,
                        )
                    else:
                        return ResponseHandling.no_records()

                else:
                    return ResponseHandling.input_format_error("User is not in the given organization")                    
            else:
                return ResponseHandling.input_format_error("user and organziation are mandatory fields")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))