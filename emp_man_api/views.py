from urllib import response
from webbrowser import get
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
    DestroyAPIView
)

from .serializers import (
    DeleteEmployeeSerializer,
    UserRegisterSerializer,
    EmployeeRegisterSerializer,
    LoginSerializer,
    EmployeeProfileSerializer,
    UpdateEmployeeSerializer,
    DeleteEmployeeSerializer,
    UsersListSerializer,
    LoginSerializer
    )


# Create your views here.


#generate token manually
def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }



class SuperManagerRegistration(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data = request.data)
        print(request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            token = get_tokens(user)
            response={
                'message':'registration successfull ',
                'user':serializer.data,
                'token':token
            }

            return Response(response,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class EmployeeRegistration(CreateAPIView):
    serializer_class = EmployeeRegisterSerializer
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        user = request.user
        if user.is_manager==True:
            print("request data : ",request.data)
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save()

                response={
                'message':'Employee Registered successfully ',
                'user':serializer.data,
                }

                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:

            response={'message':'You Dont have permissions to create Employee'}
            return Response(response,status=status.HTTP_403_FORBIDDEN)




class UserLogin(GenericAPIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.data.get('email')
            password  = serializer.data.get('password')

            user = authenticate(email= email, password  = password)
            
            if user is not None:

                token  = get_tokens(user)

                response = {
                    'message':'Login Successfull',
                    'user':email, 
                    'token':token,
                       
                }

                return Response(response,status=status.HTTP_200_OK)
            else:

                response = {
                    'message':'Login Failed! Invalid Credentials',   
                }

                return Response(response,status = status.HTTP_403_FORBIDDEN)
        
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)




class UsersList(ListAPIView):
    serializer_class = UsersListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_manager==True:
            employees = CustomUser.objects.filter(is_staff=True)
            serializer =self.serializer_class(employees, many=True)
            response ={
                'messsage':"Users List",
                'Users':serializer.data
            }

            return Response(response,status=status.HTTP_200_OK)

        else:

            response = {
                'message':'Only SuperAdmin can get Users List',
            }






class EmployeeProfile(RetrieveAPIView):
    permissin_classes = [IsAuthenticated]

    def get(self,request):
        serializer = EmployeeProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)



class UpdateEmployee(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = UpdateEmployeeSerializer

    def get_queryset(self):
        id=self.kwargs['pk']
        return CustomUser.objects.filter(id=id)

    def patch(self,request,*args,**kwargs):
        user = request.user
        if user.is_manager == True:
            emp=self.get_object()

            emp.full_name = request.data["full_name"]
            emp.email = request.data["email"]
            emp.mobile = request.data["mobile"]
            emp.address = request.data["address"]
            emp.dob = request.data["dob"]

            serializer = self.get_serializer(emp,data=request.data)

            if serializer.is_valid():
                self.partial_update(serializer)

                response ={
                    'message':'Employee Updated Successfully',
                    'user':serializer.data
                }

                return Response(response,status=status.HTTP_200_OK)
        else:

            response = {
                'message':'Only Manager can Update Employee',
            }

            return Response(response,status=status.HTTP_401_UNAUTHORIZED)





class EmployeeList(ListAPIView):
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_manager==True:
            employees = CustomUser.objects.filter(is_employee=True,is_manager=False,is_superUser=False)
            serializer =self.serializer_class(employees, many=True)
            response ={
                'messsage':"Employees List",
                'employees':serializer.data
            }

            return Response(response,status=status.HTTP_200_OK)

        else:

            response = {
                'message':'Only Manager can get Employee List',
            }




        




class UserLogout(GenericAPIView):
    serializer_class = UserLogin
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Logout Successful!'}, status=status.HTTP_200_OK)