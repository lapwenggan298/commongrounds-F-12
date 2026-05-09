from django import forms
from .models import Commission, Job

class CommissionCreateForm(forms.ModelForm):
    role = forms.CharField(
        max_length=255, 
        label="Primary Role Name",
        help_text="e.g. Lead Developer, Character Illustrator, or Editor",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the role name...'})
    )
    manpower_required = forms.IntegerField(
        min_value=1, 
        label="Role Vacancies",
        help_text="How many people do you need for THIS specific role?",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 2'})
    )

    class Meta:
        model = Commission
        fields = ["title", "description", "type", "people_required", "status"]

        labels = {
            'title': 'Project Title',
            'people_required': 'Total Project Capacity',
            'type': 'Commission Category',
        }
        
        help_text = {
            'title': 'Give your commission a catchy name.',
            'description': 'Explain the project goals, requirements, and deadlines.',
            'people_required': 'Please input the maximum number of people allowed across all jobs. This will show up as the Total Manpower.',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. 2D Animated Intro'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your project in detail...'}),
            'people_required': forms.NumberInput(attrs={'placeholder': 'e.g. 100'}),
        }