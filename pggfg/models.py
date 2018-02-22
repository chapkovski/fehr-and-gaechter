from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.forms.widgets import NumberInput
from django.db import models as djmodels

doc = """
Public Good Game with Punishment (Fehr and Gaechter).
Fehr, E. and Gachter, S., 2000.
 Cooperation and punishment in public goods experiments. American Economic Review, 90(4), pp.980-994.
"""


class Constants(BaseConstants):
    name_in_url = 'pggfg'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 20
    instructions_template = 'pggfg/Instructions.html'
    endowment = 100
    efficiency_factor = 1.6
    punishment_endowment = 20
    punishment_factor = 3


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            for o in p.get_others_in_group():
                Punishment.objects.create(sender=p, receiver=o, )


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()

    def set_pd_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution / Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.pd_payoff = sum([+ Constants.endowment,
                               - p.contribution,
                               + self.individual_share,
                               ])

    def set_punishments(self):
        for p in self.get_players():
            p.set_punishment()


class Player(BasePlayer):
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    pd_payoff = models.CurrencyField(doc='to store payoff from contribution stage')

    def set_payoff(self):
        self.payoff = self.pd_payoff + Constants.punishment_endowment - self.punishment_sent - self.punishment_received

    def set_punishment(self):
        self.punishment_sent = sum([i.amount for i in self.punishments_sent.all()])
        self.punishment_received = sum(
            [i.amount for i in self.punishments_received.all()]) * Constants.punishment_factor


class Punishment(djmodels.Model):
    sender = djmodels.ForeignKey(to=Player, related_name='punishments_sent')
    receiver = djmodels.ForeignKey(to=Player, related_name='punishments_received')
    amount = models.IntegerField(validators=[MaxValueValidator(Constants.punishment_endowment),
                                             MinValueValidator(0)],
                                 null=True,
                                 )
