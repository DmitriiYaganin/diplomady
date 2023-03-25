from django.core.management import BaseCommand

from todolist.bot.models import TgUser
from todolist.bot.tg.client import TgClient
from todolist.bot.tg.schemas import Message
from todolist.goals.models import Goal, GoalCategory, BoardParticipant


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options):
        offset = 0

        print('Bot starting handling')
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)

        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle_unauthorized(self, tg_user: TgUser, msg: Message):
        self.tg_client.send_message(msg.chat.id, 'Hello!')

        code = tg_user.set_verification_code()
        self.tg_client.send_message(tg_user.chat_id, f'Your verification code: {code}!')

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        print('Authorized')
        if msg.text == '/cancel':
            tg_user.category = None
            tg_user.stage = 0
            tg_user.save()
            self.tg_client.send_message(msg.chat.id, 'Aborted!')
            return

        if tg_user.stage == 0:
            if msg.text == '/goals':
                goals = Goal.objects.filter(
                    category__board__participants__user_id=tg_user.user.id,
                    category__is_deleted=False
                ).exclude(status=Goal.Status.archived).all()
                answer = [f'{goal.id} - {goal.title}' for goal in goals]
                self.tg_client.send_message(msg.chat.id, '\n'.join(answer))
            elif msg.text == '/create':
                categories = GoalCategory.objects.filter(
                        board__participants__user_id=tg_user.user.id,
                        is_deleted=False,
                        board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
                    ).all()
                answer_string = '\n'.join([f'{category.id} - {category.title}' for category in categories])
                self.tg_client.send_message(msg.chat.id, f'Enter category \n{answer_string}')
                tg_user.stage = 1
                tg_user.save()
            else:
                self.tg_client.send_message(msg.chat.id, 'Unknown command!')
        elif tg_user.stage == 1:
            if GoalCategory.objects.filter(
                    board__participants__user_id=tg_user.user.id,
                    is_deleted=False,
                    title=msg.text).exists():
                category = GoalCategory.objects.get(
                    board__participants__user_id=tg_user.user.id,
                    is_deleted=False,
                    title=msg.text)
                tg_user.category = category
                tg_user.stage = 2
                tg_user.save()
                self.tg_client.send_message(msg.chat.id, 'Enter new goal title!')
            else:
                self.tg_client.send_message(msg.chat.id, 'Enter correct goal!')
        elif tg_user.stage == 2:
            Goal.objects.create(
                user=tg_user.user,
                category=tg_user.category,
                title=msg.text,
            )
            tg_user.category = None
            tg_user.stage = 0
            tg_user.save()
            self.tg_client.send_message(msg.chat.id, 'Your goal is created!')
