from otree.api import (
    Currency as c, currency_range, SubmissionMustFail, Submission
)
from . import views
from otree.api import Bot, SubmissionMustFail, Submission
from .models import Constants, Player
import random
import time


class PlayerBot(Bot):
    def play_round(self):

        if self.round_number == 1:
            yield (views.Intro)
        else:
            if self.group.in_round(self.round_number - 1).dropout_exists:
                return
        contribution = random.randint(0, Constants.endowment)
        if self.group.dropout_exists:
            yield (views.DropOutFinal)
        else:
            if (self.participant.vars['debug_dropout'] and
                        self.round_number == self.participant.vars['debug_when_dropout']):
                yield Submission(views.Contribute, {'contribution': contribution}, timeout_happened=True)
                self.player.refresh_from_db()
                self.group.refresh_from_db()
                self.participant.refresh_from_db()
            else:
                yield Submission(views.Contribute, {'contribution': contribution})
                yield (views.Results)
                if self.round_number == Constants.num_rounds:
                    yield (views.FinalResults)
                self.player.refresh_from_db()
                self.group.refresh_from_db()
                self.participant.refresh_from_db()

