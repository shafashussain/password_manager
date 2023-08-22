from django.http import JsonResponse


class ResponseHandling:

    def __init__(self):
        pass

    # --------------------------------------------------------------

    @staticmethod
    def create_success(data=None):
        """
        The method called when a new record is created successfully.
        :param data:
        :return:
        """
        message = {
            'status': "success",
            'code': 201,
            'message': "Created successfully.",
            'data': data
        }
        return JsonResponse(message, status=201)

    # --------------------------------------------------------------

    @staticmethod
    def success():
        """
        This method is called when a query is executed successfully.
        :return:
        """
        message = {
            'status': "success",
            'code': 200,
            'message': "Success.",
        }
        return JsonResponse(message, status=200)

    # --------------------------------------------------------------

    @staticmethod
    def retrieve_list_success(data=None, pages=None):
        """
        This method is called to fetch list of data.
        :param data:
        :param pages:
        :return:
        """
        message = {
            'status': "success",
            'code': 200,
            'message': "Retrieved successfully.",
            'data': data,
            'pages': pages
        }
        return JsonResponse(message, status=200)

    # --------------------------------------------------------------

    @staticmethod
    def bad_request(message):
        """
        The method is called when the request could not be performed
        :return:
        """
        message = {
            'status': "error",
            'code': 400,
            'message': message
        }
        return JsonResponse(message, status=400)
    
    # --------------------------------------------------------------

    @staticmethod
    def input_format_error(suggestion=None):
        """
        The method is called when datatype is mismatched or
        some required data is missed.
        """
        message = {
            "status": "error",
            "code": 422,
            "message": "Some required fields are either empty or incorrect.",
            "suggestion": suggestion,
        }
        return JsonResponse(message, status=422)
    
    # --------------------------------------------------------------

    @staticmethod
    def query_success(message):
        """
        This method is called when a query is success.
        :return:
        """
        message = {
            "status": "success",
            "code": 200,
            "message": message,
        }
        return JsonResponse(message, status=200)
    
    # --------------------------------------------------------------

    @staticmethod
    def no_records(error_message="Records unavailable."):
        """
        The method is called when table haven't any record.
        :return:
        """
        message = {
            "status": "error",
            "code": 404,
            "message": error_message,
        }
        return JsonResponse(message, status=404)

    # --------------------------------------------------------------

        # --------------------------------------------------------------

    @staticmethod
    def login_success(data=None):
        """
        This method is called when the login is successful.
        :return:
        """
        message = {
            'status': "success",
            'code': 200,
            'message': "Logged in successfully.",
            'data': data
        }
        return JsonResponse(message, status=200)

    # --------------------------------------------------------------

    @staticmethod
    def logout_success():
        """
        This method is called when the logout is successful.
        :return:
        """
        message = {
            'status': "success",
            'code': 200,
            'message': "Logged out successfully.",
        }
        return JsonResponse(message, status=200)
    
    # --------------------------------------------------------------

    @staticmethod
    def authentication_failed(message=None):
        message = {
            'status': "error",
            'code': 401,
            'message': message
        }
        return JsonResponse(message, status=401)