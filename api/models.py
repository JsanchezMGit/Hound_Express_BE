from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class Guia(models.Model):
    trackingNumber = models.CharField(max_length=15)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100, default='TBD')
    createdAt = models.DateField(auto_created=True, auto_now=True)
    updatedAt = models.DateField(auto_created=True, auto_now=True)
    currentStatus = models.CharField(max_length=20)
    def __str__ (self):
        return self.trackingNumber    
    class Meta:
        db_table = 'Guide'

class Estatus(models.Model):
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_created=True, auto_now=True)
    updatedBy = models.CharField(max_length=20)
    guide = models.ForeignKey(Guia, on_delete=models.CASCADE)
    def __str__ (self):
        return self.status
    class Meta:
        db_table = 'StatusHistory'
        verbose_name = 'Estatus'
        verbose_name_plural = 'Estatuses'

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
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    class Meta:
        db_table = 'User'