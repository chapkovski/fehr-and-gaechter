from django import forms
from .models import Player, Punishment, Constants
from django.forms import BaseInlineFormSet, ValidationError, inlineformset_factory
from django.core.validators import MaxValueValidator, MinValueValidator


class PunishmentForm(forms.ModelForm):
    class Meta:
        model = Punishment
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        punishment_endowment = kwargs['instance'].sender.punishment_endowment
        amount = self.fields['amount']
        amount.required = True
        amount.widget.attrs['min'] = 0
        amount.widget.attrs['max'] = punishment_endowment
        amount.validators = [MinValueValidator(0), MaxValueValidator(punishment_endowment)]


class PunishmentFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        amounts = []
        punishment_endowment = self.instance.punishment_endowment
        for form in self.forms:
            # your custom formset validation
            amounts.append(form.cleaned_data['amount'])
        if sum(amounts) > punishment_endowment:
            raise ValidationError(
                "In total you can't send more than {endowment} points!".format(
                    endowment=punishment_endowment))


PFormset = inlineformset_factory(Player, Punishment,
                                 formset=PunishmentFormset,
                                 form=PunishmentForm,
                                 extra=0,
                                 can_delete=False,
                                 fk_name='sender',
                                 fields=['amount'])
