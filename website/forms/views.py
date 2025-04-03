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