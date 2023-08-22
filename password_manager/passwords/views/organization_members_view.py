from rest_framework.views import APIView

from passwords.models.user_model import UserModel
from passwords.serializers.user_serializer import UserSerializer

from password_manager.responses.response_handling import ResponseHandling


class OrganizationMembersView(APIView):

    @staticmethod
    def post(request):
        try:
            payload = request.data.dict()
            if "user" in payload and "organization" in payload:
                UserModel.objects.filter(
                    primary_key=payload["user"]
                ).update(organization=payload["organization"])
                return ResponseHandling.query_success("User added to organization")
            else:
                return ResponseHandling.input_format_error("User and organization are mandatory fields")

        except Exception as e:
            return ResponseHandling.bad_request(str(e))
   
    # ------------------------------------------------------------------------------------

    @staticmethod
    def get(request):
        """
        Used to fetch organization members
        """
        try:
            payload = request.GET.dict()

            if "primary_key" in payload:
                users = UserModel.objects.filter(organization=payload["primary_key"])
                serializer = UserSerializer(users, many=True)

                if len(serializer.data):
                    return ResponseHandling.retrieve_list_success(
                        serializer.data,
                    )
                else:
                    return ResponseHandling.no_records()
            else:
                return ResponseHandling.input_format_error("Primary key is mandatory field")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))
