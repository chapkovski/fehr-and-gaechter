from otree.api import (
    Currency as c, currency_range, SubmissionMustFail, Submission
)
from .pages import *
from otree.api import Bot, SubmissionMustFail, Submission
from .models import Constants, Player
import random
import time


class PlayerBot(Bot):
    def _cq_data(self):
        q = self.player.punishments_sent.all()
        name = 'punishments_sent'
        field_name = 'amount'
        full_answers = {}
        for i, j in enumerate(q):
            full_answers[f'{name}-{i}-id'] = j.id
            full_answers[f'{name}-{i}-owner'] = self.player.pk
            full_answers[f'{name}-{i}-{field_name}'] = random.choice([0, 1])
        return {
            f'{name}-TOTAL_FORMS': q.count(),
            f'{name}-INITIAL_FORMS': q.count(),
            f'{name}-MIN_NUM_FORMS': '0',
            f'{name}-MAX_NUM_FORMS': '1000',
            **full_answers
        }

    def play_round(self):
        if self.subsession.round_number == 1:
            yield Intro,
        yield Contribute, dict(contribution=random.randint(0, Constants.endowment))
        yield Submission(Punishment, self._cq_data(), check_html=False)
        yield Results,
