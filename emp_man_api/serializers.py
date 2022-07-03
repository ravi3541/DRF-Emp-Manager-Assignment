from ast import Pass
from distutils.sysconfig import customize_compiler
from unittest.util import _MAX_LENGTH
from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers

from emp_man_api.utils import Util
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth import authenticate


from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = (
            'email',
            'mobile',
            'full_name',
            'address',
            'dob',
            'is_superAdmin',
            'is_manager',
            'password'
        )

        extra_kwargs={
            'password':{'write_only':True}
        }

    default_error_messages={
        'permission_denied':'ONLY MANAGER CAN CREATE EMPLOYEE'
    }



    
    def create(self,validated_data):
        if validated_data['is_superAdmin']==True and validated_data['is_manager']==False:
            new_user =CustomUser.objects.create_superuser(**validated_data)
            return new_user

        elif validated_data['is_superAdmin']==False and validated_data['is_manager']==True:
            new_user =CustomUser.objects.create_Manager(**validated_data)

            return new_user
        else:
            self.fail('permission_denied')





class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = (
            'email',
            'mobile',
            'full_name',
            'address',
            'dob',
        )

       

    
    def create(self,validated_data):

        random_password = CustomUser.objects.make_random_password(8)
        print("------------Employee Password = ",random_password)

        #Send Email
        body = 'Welcome '+ validated_data['full_name'] +' \n Thanks for joining us at One stop. \n Here Are Your Login Details \n Email: '+ validated_data['email'] +'\n Password: '+ random_password 

        data = {
            'subject':'Reset Password Link, Expires in 10 min',
            'body':body,
            'to_email':validated_data['email']
        }

        Util.send_mail(data)
    
        new_employee =CustomUser.objects.create_Employee(**validated_data,password = random_password)
        return new_employee



class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','full_name','address','mobile','dob']



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = CustomUser
        fields = ['email','password']



class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','full_name','address','mobile','dob']



class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','full_name','mobile','address','dob']



class DeleteEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','is_manager','is_superAdmin']



class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    new_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)


    class Meta:
        fields=['email','old_password','new_password']

    def validate(self, attrs):
        email = attrs.get('email')
        old_pwd = attrs.get('old_password')
        new_pwd = attrs.get('new_password')

       
        user = authenticate(email= email, password  = old_pwd)
        
        if user is not None:
            user.set_password(new_pwd)
            user.save()
           
        
        else:
            raise ValidationError("Incorrect Email or Old Password")
        
        return attrs



class SendPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']

    def validate(self,attrs):
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID = ',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token = ',token)
            link = 'http://127.0.0.1:8000/api/accounts/reset-password/'+uid+'/'+token
            print('Password reset Link = ',link)

            #Send Email
            body = 'CLick this link to Reset Password '+link+' this link will automatically expire in 10 min'

            data = {
                'subject':'Reset Password Link, Expires in 10 min',
                'body':body,
                'to_email':user.email
            }

            Util.send_mail(data)


            return attrs

        else:
            raise ValidationError('You are not a registered user')


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password']

    def validate(self, attrs):
        password = attrs.get('password')
        uid = self.context.get('uid')
        token = self.context.get('token')

        id = smart_str(urlsafe_base64_decode(uid)) 
        # token = smart_str(urlsafe_base64_decode(token))

        user = CustomUser.objects.get(id = id)
        valid_token = PasswordResetTokenGenerator().check_token(user,token)

        if valid_token:
            user.set_password(password)
            user.save()

        else:
            raise ValidationError("Token is Invalid or Expired")
        
        return attrs


        