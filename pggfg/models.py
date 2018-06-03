from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from django import forms
from django.forms.widgets import NumberInput
from django.db import models as djmodels
from django.db import models as djmodels
from django.db.models import F
import json

author = "Philip Chapkovski, chapkovski@gmail.com"

doc = """
 multi-round real effort task + public good game with Punishment (Fehr and Gaechter).
 Fehr, E. and Gachter, S., 2000.
 Cooperation and punishment in public goods experiments. American Economic Review, 90(4), pp.980-994.

"""


class Constants(BaseConstants):
    name_in_url = 'pggfg'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 20
    instructions_template = 'pggfg/Instructions.html'
    endowment = 20
    efficiency_factor = 1.6
    punishment_endowment = 10
    punishment_factor = 3
    ########## RET #########
    fee = c(10)
    task_time = 60
    lb = 30
    ub = 99
    alldigs = list(range(30, 99, 1))
    # we filter out the numbers divisible by 5 to make it a bit more complicated
    rchoices = [i for i in alldigs if i % 5 != 0]


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            for o in p.get_others_in_group():
                Punishment.objects.create(sender=p, receiver=o, )
            if not self.session.config.get('ret'):
                p.endowment = Constants.endowment


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()

    def set_pd_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution / Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.pd_payoff = sum([+ p.endowment,
                               - p.contribution,
                               + self.individual_share,
                               ])

    def set_punishments(self):
        for p in self.get_players():
            p.set_punishment()


class Player(BasePlayer):
    endowment = models.CurrencyField(doc='ret earnings stored here')
    tasks_dump = models.LongStringField(doc='to store all tasks with answers')

    contribution = models.CurrencyField(
        min=0,
        doc="""The amount contributed by the player""",
    )
    punishment_sent = models.CurrencyField()
    punishment_received = models.CurrencyField()
    pd_payoff = models.CurrencyField(doc='to store payoff from contribution stage')
    punishment_endowment = models.CurrencyField(initial=0, doc='punishment endowment')

    def set_payoff(self):
        self.payoff = self.pd_payoff - self.punishment_sent - self.punishment_received

    def set_punishment_endowment(self):
        assert self.pd_payoff is not None, 'You have to set pd_payoff before setting punishment endowment'
        self.punishment_endowment = min(self.pd_payoff, Constants.punishment_endowment)

    def set_punishment(self):
        self.punishment_sent = sum([i.amount for i in self.punishments_sent.all()])
        self.punishment_received = sum(
            [i.amount for i in self.punishments_received.all()]) * Constants.punishment_factor

    ######### for RET ##########
    def get_unfinished_task(self):
        unfinished_tasks = self.tasks.filter(answer__isnull=True)
        if unfinished_tasks.exists():
            return unfinished_tasks.first()
        return False

    @property
    def finished_tasks(self):
        return self.tasks.filter(answer__isnull=False)

    def get_correct_tasks(self):
        return self.tasks.filter(correct_answer=F('answer'))

    @property
    def num_tasks_correct(self):
        return self.get_correct_tasks().count()

    def dump_tasks(self):
        q = self.finished_tasks
        data = list(q.values(
            'correct_answer',
            'answer', ))
        self.tasks_dump = json.dumps(data)

    def set_endowment(self):
        if self.session.config.get('ret'):
            self.endowment = Constants.fee * self.num_tasks_correct
        else:
            self.endowment = Constants.endowment


class Punishment(djmodels.Model):
    sender = djmodels.ForeignKey(to=Player, related_name='punishments_sent')
    receiver = djmodels.ForeignKey(to=Player, related_name='punishments_received')
    amount = models.IntegerField(null=True, )


class Task(djmodels.Model):
    player = djmodels.ForeignKey(to=Player, related_name='tasks')
    correct_answer = models.IntegerField(doc='right answer')
    answer = models.IntegerField(doc='user\'s answer', null=True)
    left = models.IntegerField(doc='for left number to sum')
    right = models.IntegerField(doc='for right number to sum')

    def get_dict(self):
        # this method is needed to push the task to the page via consumers
        return {
            "left": self.left,
            "right": self.right,
            "correct_answer": self.correct_answer,
        }
