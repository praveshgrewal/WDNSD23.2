from django import forms


class EmailForm(forms.Form):
    word_count = forms.FloatField(
        label='Word Count',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 150'})
    )
    num_links = forms.IntegerField(
        label='Number of Links',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3'})
    )
    num_exclamations = forms.IntegerField(
        label='Number of Exclamation Marks',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5'})
    )
    capital_ratio = forms.FloatField(
        label='Capital Letter Ratio (0.0 – 1.0)',
        min_value=0.0, max_value=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 0.35'})
    )
    special_char_ratio = forms.FloatField(
        label='Special Character Ratio (0.0 – 1.0)',
        min_value=0.0, max_value=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 0.12'})
    )
    has_html = forms.ChoiceField(
        label='Contains HTML',
        choices=[('1', 'Yes'), ('0', 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    email_length = forms.FloatField(
        label='Email Length (characters)',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 300'})
    )
    sender_score = forms.FloatField(
        label='Sender Reputation Score (0 – 100)',
        min_value=0.0, max_value=100.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g. 45.0'})
    )
