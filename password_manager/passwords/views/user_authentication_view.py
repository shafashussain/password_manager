from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from rest_framework.views import APIView

from passwords.models.user_model import UserModel, UserLoginModel
from passwords.serializers.user_serializer import UserLoginSerializer
from password_manager.responses.response_handling import ResponseHandling


class UserAuthenticationView(APIView):

    @staticmethod
    @csrf_exempt
    def login(request):
        """
        Used to authenticate user
        """
        try:
            if request.method == "POST":
                user = UserModel.objects.get(username=request.POST["username"])
                user_login = UserLoginModel.objects.get(
                    user=user,
                    password=request.POST["password"]
                )
                if user_login is not None:
                    # Password will be expired in 30 days
                    if date.today() - user_login.last_password_updated.date() == timedelta(days=30):
                        return ResponseHandling.bad_request("Password is Expired. Please update password")
                    else:
                        login(request, user)
                        serializer = UserLoginSerializer(user_login)
                        return ResponseHandling.login_success(serializer.data)

                return ResponseHandling.authentication_failed("Invalid Credentials")
            else:
                return ResponseHandling.bad_request("Request method is not allowed")
        except Exception as e:
            return ResponseHandling.bad_request(str(e))

    # ----------------------------------------------------------------

    # @staticmethod
    # def logout(request):
    #     """
    #     Used to logout admin user
    #     """
    #     try:
    #         if request.method == "POST":
    #             logout(request)
    #             return ResponseHandling.logout_success()
    #         else:
    #             return ResponseHandling.bad_request("Request method is not allowed")
    #     except Exception as e:
    #         return ResponseHandling.bad_request(str(e))