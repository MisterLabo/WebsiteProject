from django.db import models

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
    requested_by = models.CharField(max_length=100)

    def __str__(self):
        return self.proposed_title