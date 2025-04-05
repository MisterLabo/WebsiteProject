from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

# Display the form
@permission_required('forms.can_submit_request', raise_exception=True)
def form_display(request):
    return render(request, 'form.html')

# Handle form submission
@permission_required('forms.can_submit_request', raise_exception=True)
def submit_request(request):
    if request.method == "POST":
        # Process the form data
        messages.success(request, "Request submitted successfully!")
        return redirect('form')  # Replace 'form' with the name of your form's URL pattern

@permission_required('forms.can_view_employee_section', raise_exception=True)
def employee_section_view(request):
    # Logic for Employee Section
    return render(request, 'forms/employee_section.html')

@permission_required('forms.can_view_section_manager_section', raise_exception=True)
def section_manager_section_view(request):
    # Logic for Section Manager Section
    return render(request, 'forms/section_manager_section.html')