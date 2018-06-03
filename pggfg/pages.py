from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, Player


class Intro(Page):
    template_name = 'pggfg/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class AfterContribWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_pd_payoffs()
        for p in self.group.get_players():
            p.set_punishment_endowment()


class Punishment(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['pun{}'.format(p.id_in_group) for p in self.player.get_others_in_group()]

    def vars_for_template(self):
        others = self.player.get_others_in_group()
        form = self.get_form()
        data = zip(others, form)
        return {'data': data}

    def error_message(self, values):
        tot_pun = sum([int(i) for i in values.values()])
        if tot_pun > self.player.punishment_endowment:
            return 'You can\'t send more than {} in total'.format(self.player.punishment_endowment)


class AfterPunishmentWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_punishments()
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    ...


# from customwp.views import StartWP
page_sequence = [
    Intro,
    Contribute,
    AfterContribWP,
    Punishment,
    AfterPunishmentWP,
    Results,
]
