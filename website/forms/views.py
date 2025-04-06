from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

# Display the request form
@permission_required('forms.can_submit_request', raise_exception=True)
def form_display(request):
    return render(request, 'requestForm.html')  # Corrected template path

# Handle request form submission
@permission_required('forms.can_submit_request', raise_exception=True)
def submit_request(request):
    if request.method == "POST":
        # Process the form data
        messages.success(request, "Request submitted successfully!")
        return redirect('forms:request')

# Display the manager approval form
@permission_required('forms.can_approve_request', raise_exception=True)
def manager_approval(request):
    return render(request, 'approvalForm.html')  # Corrected template path

# Display the designer form
@permission_required('forms.can_fill_receiver_section', raise_exception=True)
def receiver_action(request):
    return render(request, 'designerForm.html')  # Corrected template path

# Display the validation form
@permission_required('forms.can_validate_request', raise_exception=True)
def validation_action(request):
    return render(request, 'validationForm.html')  # Corrected template path