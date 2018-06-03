from channels.generic.websockets import WebsocketConsumer
from pggfg.models import Player, Task
import json
import random
from pggfg.models import Constants


class TaskTracker(WebsocketConsumer):
    url_pattern = (
        r'^/tasktracker' +
        '/participant/(?P<participant_code>[a-zA-Z0-9_-]+)' +
        '/player/(?P<player>[0-9]+)' +
        '$')

    def clean_kwargs(self, kwargs):
        self.player = self.kwargs['player']
        self.participant = self.kwargs['participant_code']

    def get_player(self):
        return Player.objects.get(participant__code__exact=self.participant, pk=self.player)

    def create_task(self, player):
        left, right = random.sample(Constants.rchoices, 2)
        correct_answer = left + right
        task = player.tasks.create(left=left, right=right, correct_answer=correct_answer)
        return task.get_dict()

    def get_task(self):
        # here we check if a Player has an unanswered=unfinished task. If yes we return it as a dictionary,
        # if not - we create a new one and pass it
        player = self.get_player()
        unfinished_task = player.get_unfinished_task()
        task = unfinished_task.get_dict() if unfinished_task else self.create_task(player)
        task.update({
            'tasks_attempted': player.finished_tasks.count(),
            'tasks_correct': player.num_tasks_correct,
        })
        return task

    def receive(self, text=None, bytes=None, **kwargs):
        self.clean_kwargs(kwargs)
        jsonmessage = json.loads(text)
        response = dict()
        player = self.get_player()
        if jsonmessage.get('answer'):
            # if the request contains task answer, we process the answer
            answer = jsonmessage.get('answer')
            task = player.get_unfinished_task()
            if task:
                task.answer = answer
                task.save()
                response = self.get_task()
        self.send(response)

    def connect(self, message, **kwargs):
        self.clean_kwargs(kwargs)
        self.send(self.get_task())

    def send(self, content):
        self.message.reply_channel.send({'text': json.dumps(content)})
