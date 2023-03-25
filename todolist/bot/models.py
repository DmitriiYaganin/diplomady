import os

from django.db import models

from todolist.core.models import User
from todolist.goals.models import GoalCategory


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=50, null=True, blank=True, default=None)
    category = models.ForeignKey(GoalCategory, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    stage = models.PositiveSmallIntegerField(default=0)

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def set_verification_code(self) -> str:
        code = self._generate_verification_code()
        self.verification_code = code
        self.save(update_fields=('verification_code', ))
        return code
