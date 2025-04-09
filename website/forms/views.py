from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Request
from .forms import RequestForm

# Display the request form
def form_display(request):
    return render(request, 'requestForm.html')  # Corrected template path

# Handle request form submission
def submit_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = Request(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                submitted_by=request.user,
            )
            request_instance.save()
            messages.success(request, "Request submitted successfully!")
            return redirect('forms:request')
    else:
        form = RequestForm()
    return render(request, 'requestForm.html', {'form': form})

# Display the manager approval form
def manager_approval(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id)
    if request.method == "POST":
        form = RequestForm(request.POST, instance=request_instance)
        if form.is_valid():
            request_instance.is_approved = form.cleaned_data['is_approved']
            request_instance.reviewer_comments = form.cleaned_data['reviewer_comments']
            request_instance.reviewed_by = request.user
            request_instance.approval_date = form.cleaned_data.get('approval_date')
            request_instance.save()
            messages.success(request, "Request updated successfully!")
            return redirect('forms:approval')
    else:
        form = RequestForm(instance=request_instance)
    return render(request, 'approvalForm.html', {'form': form, 'request_instance': request_instance})

# Display the designer form
def receiver_action(request):
    return render(request, 'designerForm.html')  # Corrected template path

# Display the validation form
def validation_action(request):
    return render(request, 'validationForm.html')  # Corrected template path