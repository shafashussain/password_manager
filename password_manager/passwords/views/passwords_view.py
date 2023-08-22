from rest_framework.views import APIView

from passwords.models.user_model import UserLoginModel, UserModel
from passwords.serializers.user_serializer import UserLoginSerializer

from password_manager.responses.response_handling import ResponseHandling


class PasswordsView(APIView):

    @staticmethod
    def get(request):
        """
        Used to fetch update passwords
        """
        try:
            payload = request.GET.dict()
            requested_by = payload.pop("requested_by")
            requested_user = UserModel.objects.get(primary_key=requested_by)
            user = payload.pop("user", None)
            if requested_user.is_admin or str(requested_user.primary_key) == user:
                passwords = UserLoginModel.objects.filter(**payload)
                serializer = UserLoginSerializer(passwords, many=True)

                if len(serializer.data):
                    return ResponseHandling.retrieve_list_success(
                        serializer.data,
                    )
                else:
                    return ResponseHandling.no_records()
            else:
                return ResponseHandling.input_format_error("Either Respective User or Admin can get password details")

        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ----------------------------------------------------------------

    @classmethod
    def patch(self, request):
        """
        Used to update user passwords
        """
        try:
            payload = request.POST.dict()
            if "user" in payload and "requested_by" in payload:
                requested_by = payload.pop("requested_by")

                requested_user = UserModel.objects.get(primary_key=requested_by)
                if requested_user.is_admin or str(requested_user.primary_key) == payload["user"]:
                    get_data = UserLoginModel.objects.get(
                        user=payload["user"]
                    )
                    serializer = UserLoginSerializer(get_data, data=payload, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return ResponseHandling.query_success("Password is Updated Successfully")
                    return ResponseHandling.bad_request(serializer.errors)
                else:
                    return ResponseHandling.input_format_error("Either Respective User or Admin can only update password details")
            else:
                return ResponseHandling.input_format_error("user and requested_by are mandatory fields")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ------------------------------------------------------------------------------------
    @staticmethod
    def delete(request):
        """
        Used to delete user passwords
        """
        try:
            payload = request.data.dict()
            if "user" in payload and "requested_by" in payload:
                requested_by = payload.pop("requested_by")
                requested_user = UserModel.objects.get(primary_key=requested_by)

                if requested_user.is_admin or str(requested_user.primary_key) == payload["user"]:
                    get_data = UserLoginModel.objects.get(
                        user=payload["user"]
                    )
                    get_data.delete()
                    return ResponseHandling.query_success("Password is Deleted Successfully")
                else:
                    return ResponseHandling.input_format_error("Either Respective User or Admin can only delete password details")
            else:
                return ResponseHandling.input_format_error("user and requested_by are mandatory fields")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))
