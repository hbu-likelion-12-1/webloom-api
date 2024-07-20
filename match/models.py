from django.db import models
from users.models import User
import string
import random

class InviteCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True, db_comment="초대 코드")
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        related_name="creator",
        on_delete=models.SET_NULL,
        db_comment="생성한 유저",
        null=True,
    )

    @staticmethod
    def generate_random_code(length=6):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_random_code()
        super().save(*args, **kwargs)


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    female = models.ForeignKey(
        User,
        related_name="female",
        on_delete=models.SET_NULL,
        db_comment="아내",
        null=True,
    )
    male = models.ForeignKey(
        User, related_name="male", on_delete=models.SET_NULL, db_comment="남편", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_comment="매칭 체결일")
