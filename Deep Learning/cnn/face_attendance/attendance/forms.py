from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    """Form for registering a new employee."""

    class Meta:
        model = Employee
        fields = ['name', 'email', 'department']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter full name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter email address',
                'autocomplete': 'email',
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter department (optional)',
            }),
        }
