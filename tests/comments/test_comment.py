# import pytest
#
# from django.contrib.auth import get_user_model
# from mixer.backend.django import mixer
#
# from todolist.goals.models import GoalComment
# from todolist.goals.serializers import GoalCommentSerializer


# from myapp.serializers import GoalCommentSerializer
# from myapp.views import GoalCommentView

#
# @pytest.fixture
# def goal_comment(auth_client):
#     return mixer.blend(GoalComment, user=auth_client)
#
#
# @pytest.mark.django_db
# def test_goal_comment_view(client, auth_client, goal_comment):
#     client.force_authenticate(user=auth_client)
#     response = client.get(f'/api/goal_comment/{goal_comment.id}/')
#     assert response.status_code == 200
#     serializer = GoalCommentSerializer(goal_comment)
#     assert response.data == serializer.data
