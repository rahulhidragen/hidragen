import json
from django.http import JsonResponse
import jwt

# For checking if the product is existing to prevent the deletion of a category
class CustomProductExistError(Exception):
    def __init__(self, status=402, data={}):
        message = "Category cannot be removed as a product already exist under this category"
        self.message = message
        self.status = status
        self.data = data
        super().__init__(message)

    def to_dict(self):
        return {
            'status': self.status,
            'data': self.data,
            'message': self.message,
        }
    
# Prevention of user creation if the username already exists
class CustomUserExistError(Exception):
    def __init__(self, status=500, data={}):
        message = "User already exist, plaese choose a different username"
        self.message = message
        self.status = status
        self.data = data
        super().__init__(message)

    def to_dict(self):
        return {
            'status': self.status,
            'data': self.data,
            'message': self.message,
        }
    
# Prevention of login if the user does not exist
class CustomUserCheckError(Exception):
    def __init__(self, status=404, data={}):
        message = "User not found, please create a user to continue"
        self.message = message
        self.status = status
        self.data = data
        super().__init__(message)

    def to_dict(self):
        return {
            'status': self.status,
            'data': self.data,
            'message': self.message,
        }
    
# Validation check for the required fields
class CustomValidationError(Exception):
    def __init__(self, message, status=401, data={}):
        self.message = message
        self.status = status
        self.data = data
        super().__init__(message)

    def to_dict(self):
        return {
            'status': self.status,
            'data': self.data,
            'message': self.message,
        }
    

# Authentication error for username and password check while loggin in
class CustomAuthenticationError(Exception):
    def __init__(self, status=401, data={}):
        message = "Incorrect password/username"
        self.message = message
        self.status = status
        self.data = data
        super().__init__(message)

    def to_dict(self):
        return {
            'status': self.status,
            'data': self.data,
            'message': self.message,
        }



# Middleware class for the check of JWT status
class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            excluded_paths = ['/login/', '/create/user/']
            if request.path_info in excluded_paths:
                return self.get_response(request)

            token = request.headers.get('jwt')
            if not token:
                resp = {
                    "resp_type": "failure",
                    "message": "Token not provided"
                }
                return JsonResponse(resp, status=401)
            secret_key = "00000"
            try:
                decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                request.user = decoded_payload['username']
            except jwt.ExpiredSignatureError:
                resp = {
                    "resp_type": "failure",
                    "message": "Token Expired"
                }
                return JsonResponse(resp, status=401)
            except jwt.InvalidTokenError:
                resp = {
                    "resp_type": "failure",
                    "message": "Invalid Token"
                }
                return JsonResponse(resp, status=401)
            except CustomValidationError as e:
                resp = {
                    "resp_type": "failure",
                    "message": str(e)
                }
                return JsonResponse(resp, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
        return self.get_response(request)
    



class RequestValidation:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.path_info == "/create/category/":
                required_fields = ['name', 'description']
            elif request.path_info == "/create/user/":
                required_fields = ['username', 'password', 'name', 'email']
            elif request.path_info == "/login/":
                required_fields = ['username', 'password']
            elif request.path_info == "/create/product/":
                required_fields = ['name', 'description', 'category_id', 'image']
            elif request.path_info == "/delete/category/":
                required_fields = ['id']
            elif request.path_info == "/update/product/":
                required_fields = ['id', 'name', 'description', 'category_id']
            inputData = json.loads(request.body)
            for field in required_fields:
                if field not in inputData:
                    resp = {
                    "resp_type": "failure",
                    "message": "Missing field "+field
                    }
                    return JsonResponse(resp, status=400)
        except Exception as e:
            print("An error occurred:", str(e))
        return self.get_response(request)
