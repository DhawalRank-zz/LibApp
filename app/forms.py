from django import forms

from app.models import Suggestion

TYPE_CHOICES = (
    (1, 'Book'),
    (2, 'DVD'),
    (3, 'Other'),
)


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ['num_interested']
        labels = {'cost': 'Estimated cost in $'}

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'required': True, 'max_length': 100, 'class': 'form-control inline'}))
    pubyr = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control"}))
    type = forms.RadioSelect()
    cost = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})),
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


class SearchlibForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Title"}),
                            label="")
    author = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Author/Maker"}), label="")


class LoginForm(forms.Form):
    username = forms.CharField(widget=
                               forms.TextInput(
                                   attrs={'required': True, 'class': 'form-control', 'placeholder': 'Enter Username'}),
                               label="")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="")
