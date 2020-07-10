from otree.api import (
    Currency as c, currency_range, SubmissionMustFail, Submission
)
from pages import *
from otree.api import Bot, SubmissionMustFail, Submission
from .models import Constants, Player
import random
import time


class PlayerBot(Bot):
    def play_round(self):
        pass


