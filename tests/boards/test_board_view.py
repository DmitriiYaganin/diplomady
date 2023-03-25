import pytest
from django.urls import reverse
from rest_framework import status

from todolist.goals.models import BoardParticipant


@pytest.mark.django_db()
class TestBoardRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required_board(self, client):
        """
        Тест проверяет: неавторизованного пользователя не может просматривать доски, получит ошибку 403 авторизации.
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_board(self, auth_client, board):
        """
        Тест проверяет: можно ли смотреть удаленную доску, получит ошибку 404 страница не найдена.
        """
        board.is_deleted = True
        board.save()

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_failed_to_retrieve_foreign_board(self, client, user_factory):
        """
        Тест проверяет: пользователь не является участником доски, получит ошибку 403.
        """
        another_user = user_factory.create()
        client.force_login(another_user)

        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
class TestBoardDestroyView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """
        Тест проверяет: неавторизованного пользователя не может просматривать доски, получит ошибку 403 авторизации.
        """
        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader,
    ], ids=['writer', 'reader'])
    def test_not_owner_failed_to_delete_board(self, client, user_factory, board, board_participant_factory, role):
        """
        Тест проверяет: Не владелец, не может удалить доску, получит ошибку 403 авторизации.
        """
        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)

        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_have_to_delete_board(self, auth_client, board):
        """
        Тест проверяет: Владелец может удалить доску, получит ошибку 204 нет контента.
        """

        response = auth_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        board.refresh_from_db()
        assert board.is_deleted is True
