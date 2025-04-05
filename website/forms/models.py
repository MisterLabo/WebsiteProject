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