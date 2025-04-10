from django import forms
from .models import RequestForm
from django.contrib.auth.models import User

class RequestFormForm(forms.ModelForm):
    class Meta:
        model = RequestForm
        fields = ['request_type', 'proposed_title', 'request_date', 'purpose', 'uploaded_file']
        widgets = {
            'request_date': forms.DateInput(attrs={'type': 'date'}),
            'purpose': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the purpose of the request...'}),
        }
        help_texts = {
            'uploaded_file': 'Optional. Upload relevant documents (PDF, DOCX, etc.).',
        }

    def clean_request_date(self):
        request_date = self.cleaned_data.get('request_date')
        if request_date and request_date > forms.fields.datetime.date.today():
            raise forms.ValidationError("Request date cannot be in the future.")
        return request_date

    def clean_uploaded_file(self):
        uploaded_file = self.cleaned_data.get('uploaded_file')
        if uploaded_file and uploaded_file.size > 5 * 1024 * 1024:  # 5 MB limit
            raise forms.ValidationError("File size must not exceed 5 MB.")
        return uploaded_file

class SupervisorReviewForm(forms.ModelForm):
    class Meta:
        model = RequestForm
        fields = ['supervisor_status']
        widgets = {
            'supervisor_status': forms.RadioSelect(choices=RequestForm.SUPERVISOR_CHOICES),
        }

class EngineerAssignForm(forms.ModelForm):
    class Meta:
        model = RequestForm
        fields = ['assigned_engineer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit choices to users in the 'Engineer' group
        self.fields['assigned_engineer'].queryset = User.objects.filter(groups__name='Engineer')
        self.fields['assigned_engineer'].label = "Assign Engineer"
        self.fields['assigned_engineer'].help_text = "Select an engineer to assign to this request."

    def clean_assigned_engineer(self):
        assigned_engineer = self.cleaned_data.get('assigned_engineer')
        if not assigned_engineer:
            raise forms.ValidationError("You must select an engineer to assign.")
        return assigned_engineer

# Uncomment and enhance if needed
# class ApprovalForm(forms.ModelForm):
#     class Meta:
#         model = RequestForm
#         fields = ['approval_status']
#         widgets = {
#             'approval_status': forms.RadioSelect(choices=[('approved', 'Approve'), ('rejected', 'Reject')]),
#         }