from django import forms

class RequestForm(forms.Form):
    # Fields for the request form
    title = forms.CharField(max_length=100, required=True, label="Request Title")
    description = forms.CharField(widget=forms.Textarea, required=True, label="Description")
    submitted_by = forms.CharField(max_length=50, required=True, label="Submitted By")
    
    # Approval or rejection fields
    is_approved = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        required=False,
        label="Approval Status"
    )
    approval_date = forms.DateField(required=False, label="Approval Date")
    reviewed_by = forms.CharField(max_length=50, required=False, label="Reviewed By")
    
    # Review and assignment fields
    reviewer_comments = forms.CharField(
        widget=forms.Textarea, required=False, label="Reviewer Comments"
    )
    assigned_designer = forms.CharField(
        max_length=50, required=False, label="Assigned Designer"
    )
    
    # Validation field for rating
    rating = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=5,
        label="Satisfaction Rating (1-5)"
    )

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean(self):
        cleaned_data = super().clean()
        is_approved = cleaned_data.get('is_approved')
        reviewer_comments = cleaned_data.get('reviewer_comments')

        if is_approved == 'reject' and not reviewer_comments:
            raise forms.ValidationError("Reviewer comments are required if the request is rejected.")
        return cleaned_data
