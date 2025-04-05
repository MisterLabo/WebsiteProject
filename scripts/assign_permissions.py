from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from forms.models import ContactForm

def assign_permissions():
    content_type = ContentType.objects.get_for_model(ContactForm)

    # Create groups
    section_1_group, _ = Group.objects.get_or_create(name='Section 1 Editors')
    section_2_group, _ = Group.objects.get_or_create(name='Section 2 Editors')

    # Assign permissions to groups
    section_1_permissions = [
        Permission.objects.get(codename='can_view_section_1', content_type=content_type),
        Permission.objects.get(codename='can_fill_section_1', content_type=content_type),
    ]
    section_2_permissions = [
        Permission.objects.get(codename='can_view_section_2', content_type=content_type),
        Permission.objects.get(codename='can_fill_section_2', content_type=content_type),
    ]

    section_1_group.permissions.set(section_1_permissions)
    section_2_group.permissions.set(section_2_permissions)

    print("Permissions assigned successfully.")

# Run the function
if __name__ == "__main__":
    assign_permissions()
