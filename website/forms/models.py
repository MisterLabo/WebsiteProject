from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Create your models here.

class RequestForm(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('project', 'Project'),
        ('modification', 'Modification'),
        ('drawing', 'Drawing'),
    ]
    request_type = models.CharField(
        max_length=50,
        choices=REQUEST_TYPE_CHOICES,
        default='new',
    )
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
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='checked_requests')
    assigned_engineer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    checked_at = models.DateTimeField(null=True, blank=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save

    class Meta:
        permissions = [
            ("can_approve_request", "Can approve request"),
            ("can_reject_request", "Can reject request"),
            ("can_review_supervisor", "Can review supervisor"),
            ("can_assign_engineer", "Can assign Engineer"),
        ]

    def clean(self):
        """Ensure data integrity."""
        if self.approval_status == 'approved' and self.supervisor_status == 'rejected':
            raise ValidationError("A request cannot be approved by a manager and rejected by a supervisor.")
        if self.assigned_engineer and self.approval_status != 'approved':
            raise ValidationError("Engineer cannot be assigned to a request that is not approved.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

    def approve(self, user):
        """Approve the request."""
        if self.approval_status != 'pending':
            raise ValueError("Only pending requests can be approved.")
        self.approval_status = 'approved'
        self.approved_by = user
        self.approved_at = now()
        self.save()

    def reject(self, user):
        """Reject the request."""
        if self.approval_status != 'pending':
            raise ValueError("Only pending requests can be rejected.")
        self.approval_status = 'rejected'
        self.approved_by = user
        self.approved_at = now()
        self.save()

    def assign_engineer(self, engineer, user):
        """Assign an engineer to the request."""
        if self.approval_status != 'approved' or self.supervisor_status != 'approved':
            raise ValueError("Request must be approved by both manager and supervisor before assigning an engineer.")
        if self.assigned_engineer:
            raise ValueError("Engineer is already assigned.")
        self.assigned_engineer = engineer
        self.assigned_at = now()
        self.save()

    def __str__(self):
        return f"{self.proposed_title} ({self.get_approval_status_display()})"