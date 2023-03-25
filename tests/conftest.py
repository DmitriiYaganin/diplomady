import pytest
from rest_framework.test import APIClient

from todolist.goals.models import Goal, GoalCategory, Board

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client


# @pytest.fixture
# def some_goal():
#     goal = Goal.objects.create()
#     return goal

@pytest.fixture
def some_board():
    board = Board.objects.create(title='My board')
    return board


@pytest.fixture
def some_category(some_board):
    category = GoalCategory.objects.create(board=some_board, title='My category')
    return category


@pytest.fixture
def some_goal(some_category):
    goal = Goal.objects.create(title='My goal', category=some_category)
    return goal
