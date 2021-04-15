from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models import BooleanField

class UserManager(BaseUserManager):

    def _create_user(self, email, password, usertype, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            usertype=usertype,
            is_staff=is_staff, 
            is_active=True,
            is_superuser=is_superuser, 
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_candidate(self, email, password, **extra_fields):
        return self._create_user(email, password, 1, False, False, **extra_fields)

    def create_recruiter(self, email, password, **extra_fields):
        return self._create_user(email, password, 0, False, False, **extra_fields)

    def create_staff(self, email, password, **extra_fields):
        return self._create_user(email, password, None, True, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email, password, None, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    '''
    Usertype can have 3 values:
        Candidate - 1
        Recruiter - 0
        Staff - None
    '''
    USERTYPES = [
        (1, 'Candidates'),
        (0, 'Recruiters'),
        (None, 'Staff'),
    ]

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    usertype = models.PositiveSmallIntegerField(choices=USERTYPES, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

