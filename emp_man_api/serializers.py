from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken,TokenError


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = (
            'email',
            'mobile',
            'full_name',
            'address',
            'dob',
            'is_superUser',
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
        if validated_data['is_superUser']==True and validated_data['is_manager']==False:
            new_user =CustomUser.objects.create_superuser(**validated_data)
            return new_user

        elif validated_data['is_superUser']==False and validated_data['is_manager']==True:
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
        print("Employee Password = ",random_password)
        
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
        fields = ['id','email','full_name','address','mobile','dob','is_staff','is_manager','is_superUser']





class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': 'Token is expired or invalid!'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')