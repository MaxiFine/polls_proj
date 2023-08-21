from django import forms
from .models import Polls



class PollsQuestionForm(forms.ModelForm):
    class Meta:
        model = Polls
        fields = ['question', 'pc_mail', 'option1', 'option2', 'option3',]


class SharePollForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    to = forms.EmailField()
    


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Polls
        fields = ['question', 'pc_mail', 'option1',
                  'option2','option3', 'status',]

