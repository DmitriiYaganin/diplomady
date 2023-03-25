import pytest
from django.urls import reverse
from rest_framework import status

# from todolist.goals.serializers import GoalSerializer


@pytest.mark.django_db
class TestGoalView:
    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(goal_pk: int) -> str:
        return reverse('todolist.goals:goal', kwargs={'pk': goal_pk})

    def test_auth_required_goal(self, client):
        """
        Тест проверяет: неавторизованного пользователя не может просматривать цели, получит ошибку 403 авторизации.
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    # def test_retrieve_goal(self, auth_client, some_goal):
    #
    #     response = auth_client.get(self.url)
    #
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data == GoalSerializer(some_goal).data

    # def test_update_goal(self, authenticated_client, some_goal):
    #
    #     data = {'title': 'New title'}
    #     response = authenticated_client.patch(self.url, data=data)
    #
    #     some_goal.refresh_from_db()
    #     assert response.status_code == status.HTTP_200_OK
    #     assert some_goal.title == 'New title'

    # def test_delete_goal(self, authenticated_client, some_goal):
    #
    #     response = authenticated_client.delete(self.url)
    #
    #     some_goal.refresh_from_db()
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #     assert some_goal.status
