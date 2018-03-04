from django import forms
from .models import Player, Punishment, Constants
from django.forms import BaseInlineFormSet, ValidationError, inlineformset_factory


class PunishmentForm(forms.ModelForm):
    class Meta:
        model = Punishment
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].required = True
        self.fields['amount'].widget.attrs['min'] = 0
        self.fields['amount'].widget.attrs['max'] = Constants.punishment_endowment


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
                "In total you can't send more than {endowment} points!".format(
                    endowment=Constants.punishment_endowment))


PFormset = inlineformset_factory(Player, Punishment,
                                 formset=PunishmentFormset,
                                 form=PunishmentForm,
                                 extra=0,
                                 can_delete=False,
                                 fk_name='sender',
                                 fields=['amount'])
