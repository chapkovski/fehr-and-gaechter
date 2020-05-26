from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .forms import PFormset
from .models import Constants, Player, Punishment as PunishmentModel
from otree.constants import timeout_happened


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
    timeout_seconds = 30

    def vars_for_template(self):
        return {'formset': PFormset(instance=self.player)}

    def post(self):
        context = super().get_context_data()
        auto_submitted = self.request.POST.get(timeout_happened)
        if not auto_submitted:
            formset = PFormset(self.request.POST, instance=self.player)
            context['formset'] = formset
            context['form'] = self.get_form()
            if formset.is_valid():
                allpuns = formset.save(commit=True)
            else:
                return self.render_to_response(context)
        return super().post()

    def before_next_page(self):
        if self.timeout_happened:
            self.player.punishments_sent.all().update(amount=0)


class AfterPunishmentWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_punishments()
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    ...


page_sequence = [
    Intro,
    Contribute,
    AfterContribWP,
    Punishment,
    AfterPunishmentWP,
    Results,
]
