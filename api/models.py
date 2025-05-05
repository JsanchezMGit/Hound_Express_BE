from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class Guia(models.Model):
    id = models.IntegerField(primary_key=True)
    trackingNumber = models.CharField(max_length=15)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    createdAt = models.DateField(auto_created=True, auto_now=True)
    updatedAt = models.DateField(auto_created=True, auto_now=True)
    currentStatus = models.CharField(max_length=20)
    class Meta:
        db_table = 'Guide'

class Estatus(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_created=True, auto_now=True)
    updatedBy = models.CharField(max_length=20)
    guide = models.ForeignKey(Guia, on_delete=models.CASCADE)
    class Meta:
        db_table = 'StatusHistory'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    createdAt = models.DateField(auto_created=True, auto_now=True)
    updatedAt = models.DateField(auto_created=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email
    class Meta:
        db_table = 'User'