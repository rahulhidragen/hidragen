# myapp/views.py
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from commonUtils.middleware import CustomAuthenticationError, CustomProductExistError, CustomUserCheckError, CustomUserExistError, CustomValidationError
from .models import Login, User, Category, Products
from commonUtils.jwt import encodeJwt

def hello_world(request):
    return HttpResponse("Products V.0.1 is running successfully!")

@csrf_exempt
def create_user(request):
    try:
        userData = json.loads(request.body)
        userObj = User.objects.filter(username=userData['username'])
        if userObj:
            raise CustomUserExistError()
        newUser = User()
        newUser.name = userData['name']
        newUser.username = userData['username']
        newUser.email = userData['email']
        newUser.save()
        newLogin = Login()
        newLogin.username = userData['username']
        newLogin.password = userData['password']
        newLogin.jwt = ""
        newLogin.save()
        return HttpResponse("User created successfully!")
    
    except CustomValidationError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response, status=failure_response['status'])
    except CustomUserExistError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response, status=failure_response['status'])




@csrf_exempt
def login(request):
    try:
        userData = json.loads(request.body)
        loginData = Login.objects.filter(username=userData['username'])
        if not loginData:
            raise CustomUserCheckError()
        token = encodeJwt(userData['username'])
        loginData = Login.objects.filter(username=userData['username'], password=userData['password'])
        if not loginData:
            raise CustomAuthenticationError()
        loginData = Login.objects.get(username=userData['username'])
        loginData.jwt = token
        loginData.save()
        response = {
            "username": userData['username'],
            "jwt": token
        }
        return JsonResponse(response, safe=False)
    except CustomValidationError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response)
    except CustomAuthenticationError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response)
    except CustomUserCheckError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response)



def fetch_user(request):
    users = User.objects.all()
    usersList = []
    for user in users:
        userDict = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email
        }
        logins = Login.objects.filter(username=userDict['username'])
        for i in logins:
            userDict["jwt"] = i.jwt
        usersList.append(userDict)
    return JsonResponse(usersList, safe=False)



@csrf_exempt
def create_category(request):
    categoryData = json.loads(request.body)
    try:
        newcategory = Category()
        newcategory.name = categoryData['name']
        newcategory.description = categoryData['description']
        newcategory.save()
        return HttpResponse("Category created successfully!")
    except CustomValidationError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response, status=failure_response['status'])



@csrf_exempt
def fetch_category(request):
    categories = Category.objects.all()
    categoriesList = []
    for category in categories:
        userDict = {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }
        categoriesList.append(userDict)
    return JsonResponse(categoriesList, safe=False)


@csrf_exempt
def create_product(request):
    productData = json.loads(request.body)
    try:
        category = Category.objects.filter(id=productData['category_id'])
        if not category:
            return HttpResponse("Category id invalid!")
        for i in category:
            data = { 
                "name":i.name,
                "id":i.id,
                "description":i.description
            }
        newproduct = Products()
        newproduct.name = productData['name']
        newproduct.category_id = data['id']
        newproduct.description = productData['description']
        newproduct.created_by = request.user
        newproduct.image = productData['image']
        newproduct.save()
        return HttpResponse("Product created successfully!")
    except CustomValidationError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response, status=failure_response['status'])


@csrf_exempt
def fetch_product(request):
    productData = json.loads(request.body)
    products = Products.objects.all()
    productsList = []
    for product in products:
        userDict = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'createdBy': product.created_by,
            "image":product.image
        }
        productsList.append(userDict)
    return JsonResponse(productsList, safe=False)



@csrf_exempt
def delete_category(request):
    categoryData = json.loads(request.body)
    try:
        products = Products.objects.filter(category_id=categoryData["id"])
        if products:
            raise CustomProductExistError()
        removecategory = Category.objects.filter(id=categoryData['id'])
        removecategory.delete()
        return HttpResponse("Category deleted successfully!")
    except CustomValidationError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response, status=failure_response['status'])
    except CustomProductExistError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response, status=failure_response['status'])



@csrf_exempt
def update_product(request):
    productData = json.loads(request.body)
    try:
        productToUpdate = Products.objects.get(id=productData['id'])
        productDict = productToUpdate.__dict__
        if productDict['created_by'] != request.user:
            return HttpResponse("Not created by this user")
        productToUpdate.name = productData['name']
        productToUpdate.category_id = productData['category_id']
        productToUpdate.description = productData['description']
        productToUpdate.save()
        return HttpResponse("Product updated successfully")
    except CustomValidationError as e:
        failure_response = e.to_dict()
        return JsonResponse(failure_response, status=failure_response['status'])