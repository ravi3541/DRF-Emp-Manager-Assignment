
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    mobile = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250,)
    dob = models.DateField()
    
    is_staff = models.BooleanField(default=True)
    is_superUser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','mobile',]

    def __str__(self):
        return self.email

    