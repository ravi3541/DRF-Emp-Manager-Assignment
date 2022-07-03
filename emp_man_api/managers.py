from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        print("Registering User")
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have Password')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        
        user.set_password(password)
        user.save()
        return user




    def create_Employee(self, email, password, **extra_fields):
        #Creating Employee
        print("Creating Employee")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superAdmin", False)
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_employee", True)

        return self.create_user(email, password,**extra_fields)


    
    def create_Manager(self, email, password, **extra_fields):
        #Creating Manager
        print("Creating Manager")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superAdmin", False)
        extra_fields.setdefault("is_manager", True)
        extra_fields.setdefault("is_employee", True)

        return self.create_user(email, password,**extra_fields)




    def create_superuser(self, email, password, **extra_fields):
        #Creating Super User
        print("Creating Super User")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superAdmin", True)
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_employee", True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superAdmin') is not True:
            raise ValueError('Superuser must have is_superAdmin=True.')

        return self.create_user(email, password,**extra_fields)
