from django import forms
from .models import Player, Punishment, Constants
from django.forms import BaseInlineFormSet, ValidationError, inlineformset_factory
from django.core.validators import MaxValueValidator, MinValueValidator



class PunishmentFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        amounts = []
        punishment_endowment = self.instance.punishment_endowment
        for form in self.forms:
            amounts.append(form.cleaned_data['amount'])
        if sum(amounts) > punishment_endowment:
            raise ValidationError(
                "In total you can't send more than {endowment} points!".format(
                    endowment=punishment_endowment))


PFormset = inlineformset_factory(Player, Punishment,
                                 formset=PunishmentFormset,
                                 extra=0,
                                 can_delete=False,
                                 fk_name='sender',
                                 fields=['amount'])
