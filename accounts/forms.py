from django import forms

from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name']


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'roles', 'email_address']
        widgets = {
            'roles': forms.CheckboxSelectMultiple(),
            'display_name': forms.TextInput(attrs={'placeholder': 'How should we call you?'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roles'].help_text = "Select all roles that apply to you across our applications."