from django.db import models
from users.managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .validator import validate_file_extension




class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [
        ('1','Operation'),
        ('2','Client'),
    ]
    name = models.CharField(
        _('full name'), max_length=100, blank=True, null=True)
    email = models.EmailField(_("'email address"), max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=2,choices=USER_TYPE,default=1)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class FileUpload(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, db_column='user_id', null=True, blank=True)
    file = models.FileField(upload_to='uploaded_files',validators=[validate_file_extension])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)