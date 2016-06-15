from django import forms


class SearchlibForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Title"}),
                            label="")
    author = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Author/Maker"}), label="")
