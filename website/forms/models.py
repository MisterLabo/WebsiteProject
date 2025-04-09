from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ContactForm(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('project', 'Project'),
        ('modification', 'Modification'),
        ('drawing', 'Drawing'),
    ]

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    proposed_title = models.CharField(max_length=200)
    request_date = models.DateField()
    user_requirement_specification = models.TextField()
    uploaded_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    purpose = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_employee_section", "Can view Employee Section"),
            ("can_fill_employee_section", "Can fill Employee Section"),
            ("can_view_section_manager_section", "Can view Section Manager Section"),
            ("can_fill_section_manager_section", "Can fill Section Manager Section"),
        ]

    def __str__(self):
        return self.proposed_title

class Request(models.Model):
    APPROVAL_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_requests")
    is_approved = models.CharField(max_length=10, choices=APPROVAL_CHOICES, null=True, blank=True)
    reviewer_comments = models.TextField(null=True, blank=True)
    assigned_designer = models.CharField(max_length=50, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title