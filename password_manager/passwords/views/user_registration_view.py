from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from passwords.models.user_model import UserModel, UserLoginModel
from passwords.serializers.user_serializer import UserSerializer
from password_manager.responses.response_handling import ResponseHandling


class UserRegistrationView(APIView):

    @csrf_exempt
    def post(self, request):
        """
        Used to register user
        """
        try:
            payload = request.data.dict()
            # hashing user password
            password = payload.pop("password")
            payload["user"] = request.user
            user = UserSerializer(data=payload)
            if user.is_valid():
                data = user.save()
                UserLoginModel.objects.create(user=data, password=password)
                return ResponseHandling.create_success(user.data)

            return ResponseHandling.bad_request(user.errors)
        except Exception as e:
            return ResponseHandling.bad_request(str(e))
        
    @staticmethod
    def get(request):
        """
        Used to fetch users
        Only Admin Users or the corresponsing user will get password details
        """
        try:
            payload = request.GET.dict()
            requested_by = payload.pop("requested_by")
            requested_user = UserModel.objects.get(primary_key=requested_by)

            users = UserModel.objects.filter(**payload)
            serializer = UserSerializer(users, many=True)
            response_data = serializer.data
            primary_key = payload.pop("primary_key", None)
            if len(response_data):
                if requested_user.is_admin or str(requested_user.primary_key) == primary_key:
                    for data in response_data:
                        password = UserLoginModel.objects.get(user=data["primary_key"]).password
                        data["password"] = password
                return ResponseHandling.retrieve_list_success(
                    response_data,
                )
            else:
                return ResponseHandling.no_records()

        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ----------------------------------------------------------------

    @classmethod
    def patch(self, request):
        """
        Used to update user
        Only Admin Users or the corresponsing user can update user details
        """
        try:
            payload = request.POST.dict()
            requested_by = payload.pop("requested_by")

            requested_user = UserModel.objects.get(primary_key=requested_by)
            if requested_user.is_admin or str(requested_user.primary_key) == payload["primary_key"]:
                if "primary_key" in payload:
                    get_data = UserModel.objects.get(
                        primary_key=payload["primary_key"]
                    )
                    serializer = UserSerializer(get_data, data=payload, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return ResponseHandling.query_success("User is Updated Successfully")
                    return ResponseHandling.bad_request(serializer.errors)
                else:
                    return ResponseHandling.input_format_error("Primary key is mandatory field")
            else:
                return ResponseHandling.input_format_error("Either Respective User or Admin can update the details")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ------------------------------------------------------------------------------------

    @staticmethod
    def delete(request):
        """
        Used to delete organization
        Only Admin Users or the corresponsing user can delete user details
        """
        try:
            payload = request.data.dict()
            requested_by = payload.pop("requested_by")

            requested_user = UserModel.objects.get(primary_key=requested_by)
            if requested_user.is_admin or str(requested_user.primary_key) == payload["primary_key"]:
                if "primary_key" in payload:
                    get_data = UserModel.objects.get(
                        primary_key=payload["primary_key"]
                    )
                    get_data.delete()
                    return ResponseHandling.query_success("User is Deleted Successfully")
                else:
                    return ResponseHandling.input_format_error("Primary key is mandatory field")
            else:
                return ResponseHandling.input_format_error("Either Respective User or Admin can delete the details")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))
