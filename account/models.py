from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone field must be set')
        user = self.model(phone_number=phone_number, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'OWNER')
        return self.create_user(username, phone_number, password, **extra_fields)




class UserTypes(models.TextChoices):
    OWNER = "OWNER", "Owner"
    EMPLOYEE = "EMPLOYEE", "Employee"
    CUSTOMER = "CUSTOMER", "Customer"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=20, choices=UserTypes.choices, default=UserTypes.CUSTOMER)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number"]

    def save(self, *args, **kwargs):
        
        if self.role == UserTypes.OWNER:
            self.is_staff = True
            self.is_superuser = True

        super().save(*args, **kwargs)