from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RequestForm(models.Model):
    request_type = models.CharField(max_length=50)
    proposed_title = models.CharField(max_length=100)
    request_date = models.DateField()
    purpose = models.TextField()
    uploaded_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    APPROVAL_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('checked', 'Checked'),
        ('assigned', 'Assigned'),
    ]
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='pending',
    )
    
    SUPERVISOR_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    supervisor_status = models.CharField(
        max_length=10,
        choices=SUPERVISOR_CHOICES,
        default='pending',
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    approved_at = models.DateTimeField(null=True, blank=True)
#   assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='checked_requests')
    assigned_engineer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    supervisor_status = models.CharField(max_length=10, choices=SUPERVISOR_CHOICES, default='pending')
    checked_at = models.DateTimeField(null=True, blank=True)
    assigned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_approve_request", "Can approve request"),
            ("can_reject_request", "Can reject request"),
            ("can_review_supervisor", "Can review supervisor"),
            ("can_assign_engineer", "Can assign Engineer"),
        ]

    def __str__(self):
        return self.proposed_title