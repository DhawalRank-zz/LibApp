from django import forms

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
    pubyr = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'validate', 'placeholder': 'Publication Year'}),
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
        fields = ['username', 'password', 'password1', 'first_name', 'last_name', 'email', 'address', 'city', 'province',
                  'profilepic']
        labels = {'profilepic': 'Profile Picture'}

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'validate'}), label="Password")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'validate'}), label="Confirm Password")
