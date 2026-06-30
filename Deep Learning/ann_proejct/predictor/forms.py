from django import forms

class TransactionForm(forms.Form):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    ACCOUNT_TYPE_CHOICES = [('Savings', 'Savings'), ('Checking', 'Checking'), ('Credit', 'Credit')]
    DAY_CHOICES = [
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
    TRANSACTION_TYPE_CHOICES = [('Debit', 'Debit'), ('Credit', 'Credit'), ('Transfer', 'Transfer')]
    CATEGORY_CHOICES = [
        ('Shopping', 'Shopping'), ('Bills', 'Bills'), ('Food', 'Food'),
        ('Entertainment', 'Entertainment'), ('Travel', 'Travel'), ('Other', 'Other')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Card', 'Card'), ('Bank Transfer', 'Bank Transfer'), ('Mobile Wallet', 'Mobile Wallet'),
        ('Check', 'Check'), ('Cash', 'Cash')
    ]
    DEVICE_CHOICES = [('Mobile', 'Mobile'), ('Desktop', 'Desktop'), ('Tablet', 'Tablet')]

    customer_age = forms.IntegerField(label='Age', min_value=18, max_value=120, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 45'}))
    customer_gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    account_type = forms.ChoiceField(label='Account Type', choices=ACCOUNT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    annual_income = forms.FloatField(label='Annual Income ($)', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50000'}))
    credit_score = forms.IntegerField(label='Credit Score', min_value=300, max_value=850, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 750'}))
    account_tenure_months = forms.IntegerField(label='Account Tenure (months)', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 24'}))
    transaction_hour = forms.IntegerField(label='Transaction Hour (0-23)', min_value=0, max_value=23, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 14'}))
    day_of_week = forms.ChoiceField(label='Day of Week', choices=DAY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    transaction_type = forms.ChoiceField(label='Transaction Type', choices=TRANSACTION_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    transaction_category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_METHOD_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    device_type = forms.ChoiceField(label='Device Type', choices=DEVICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.FloatField(label='Transaction Amount ($)', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 150.50'}))
    is_international = forms.BooleanField(label='International Transaction', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    account_balance_after = forms.FloatField(label='Account Balance After ($)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5000'}))
