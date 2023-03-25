import pytest
from django.urls import reverse
from rest_framework import status
from typing import Callable

# from todolist.goals.models import Goal, BoardParticipant
from todolist.goals.permissions import GoalPermissions
from todolist.goals.serializers import GoalCreateSerializer
from todolist.goals.views import GoalCreateView


@pytest.fixture()
def goals_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db
class TestGoalCreateView:
    url = reverse('todolist.goals:create-goal')
    """
    Тест проверяет: что при отправке POST-запроса на создания цели с правильными данными,
    создается новая цель и возвращается код 201.
    """

    # def test_create_goal(self, client):
    #     data = {'title': 'My new goal'}
    #
    #     response = client.post(self.url, data=data)
    #
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert Goal.objects.count() == 1
    #
    #     goal = Goal.objects.first()
    #     assert goal.title == 'My new goal'

    def test_auth_required_create_in_goal(self, client, goals_create_data):
        """
        Тест проверяет: неавторизованного пользователя при создании цели, получит ошибку 403 авторизации.
        """
        response = client.post(self.url, data=goals_create_data())

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_permission_classes(self):
        """
        Тест проверяет: что класс GoalCreateView имеет правильный набор прав доступа.
        """

        assert GoalCreateView.permission_classes == [GoalPermissions]

    def test_serializer_class(self):
        """
        Тест проверяет: что класс GoalCreateView использует правильный сериализатор для создания цели.
        """

        assert GoalCreateView.serializer_class == GoalCreateSerializer
