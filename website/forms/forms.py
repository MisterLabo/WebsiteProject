from django import forms
from .models import RequestForm
from django.contrib.auth.models import User

class RequestFormForm(forms.ModelForm):
    class Meta:
        model = RequestForm
        fields = ['request_type', 'proposed_title', 'request_date', 'purpose', 'uploaded_file']  # Or list the fields you want

class SupervisorReviewForm(forms.ModelForm):
    class Meta:
        model = RequestForm
        fields = ['supervisor_status']

class EngineerAssignForm(forms.ModelForm):
    class Meta:
        model = RequestForm
        fields = ['assigned_engineer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit choices to users in the 'Engineer' group
        self.fields['assigned_engineer'].queryset = User.objects.filter(groups__name='Engineer')


"""
class ApprovalForm(forms.ModelForm):
    class Meta: 
        model = RequestForm
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(choices=[('approved', 'Approve'), ('rejected', 'Reject')])
        }

"""