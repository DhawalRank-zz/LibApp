from django import forms
from django.utils.html import format_html

from app.models import Suggestion, Libuser, Libitem

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
            attrs={'required': True, 'max_length': 100, 'class': 'validate', 'placeholder': 'Title'}), label="")
    pubyr = forms.IntegerField(min_value=1900, max_value=2016,
                               widget=forms.NumberInput(attrs={'class': 'validate', 'placeholder': 'Publication Year'}),
                               label="")
    type = forms.CharField(widget=forms.Select(choices=TYPE_CHOICES))
    cost = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'validate', 'placeholder': 'Estimated cost in $'}), label="")
    comments = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Comments'}),
                               label="")


class SearchlibForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Title"}),
                            label="")
    author = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Author/Maker"}), label="")


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'required': True, 'class': 'validate', 'placeholder': 'Username'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': True, 'class': 'validate input-field', 'placeholder': 'Password'}),
        label="")


class Register(forms.ModelForm):
    class Meta:
        model = Libuser
        fields = ['username', 'password', 'password1', 'first_name', 'last_name', 'email', 'address', 'city',
                  'province', 'phone', 'profilepic']
        widgets = {
            'password': forms.PasswordInput()}

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'validate'}), label="Confirm Password")

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'required'
            if self.fields[key].label:
                self.fields[key].label += ' *'


class MyAcct(forms.ModelForm):
    class Meta:
        model = Libuser
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'province', 'phone', 'profilepic']

    def __init__(self, *args, **kwargs):
        super(MyAcct, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
