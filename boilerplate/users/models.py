from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .validators import PhoneNumberValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email, password=password, is_superuser=True, is_staff=True, **extra_fields
        )
        user.save(using=self._db)
        return user


# AbstractUser 이용
# class User(AbstractUser):

#     """Model definition for User."""

#     username = None
#     first_name = None
#     last_name = None

#     email = models.EmailField(  # 유저 아이디
#         unique=True, max_length=200, verbose_name="이메일", help_text="필수"
#     )
#     name = models.CharField(max_length=100, verbose_name="이름", help_text="필수")  # 유저 이름
#     phone_number = models.CharField(  # 유저 전화번호
#         validators=[PhoneNumberValidator()],
#         max_length=11,
#         unique=True,
#         verbose_name="전화번호",
#         help_text="필수",
#     )

#     objects = UserManager()  # 재정의 된 UserManager 사용 선언

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["name", "phone_number"]

#     def __str__(self):
#         return self.email

#     class Meta:
#         db_table = "user"
#         verbose_name = "회원"
#         verbose_name_plural = "회원"


# AbstractBaseUser 이용
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(  # 유저 아이디
        unique=True, max_length=200, verbose_name="이메일", help_text="필수"
    )
    name = models.CharField(max_length=100, verbose_name="이름", help_text="필수")  # 유저 이름
    phone_number = models.CharField(  # 유저 전화번호
        validators=[PhoneNumberValidator()],
        max_length=11,
        unique=True,
        verbose_name="전화번호",
        help_text="필수",
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()  # 재정의 된 UserManager 사용 선언

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_number"]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        verbose_name = "회원"
        verbose_name_plural = "회원"
