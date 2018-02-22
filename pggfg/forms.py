from django.forms import inlineformset_factory
from .models import Player, Punishment, Constants
from django.forms import BaseInlineFormSet, ValidationError


class PunishmentFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        amounts = []
        for form in self.forms:
            # your custom formset validation
            amounts.append(form.cleaned_data['amount'])
        if sum(amounts) > Constants.punishment_endowment:
            raise ValidationError(
                "In total you can't send more than {endowment} points!".format(endowment=Constants.punishment_endowment))


PFormset = inlineformset_factory(Player, Punishment,
                                 formset=PunishmentFormset,
                                 extra=0,
                                 can_delete=False,
                                 fk_name='sender',
                                 fields=['amount'])
