from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import RequestFormForm
from .models import RequestForm
from django.http import HttpResponseForbidden

# Create your views here.
def is_manager(user):
    return user.is_staff

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestFormForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
#           form.save()
            return redirect('forms:list_request')  # Or anywhere else
    else:
        form = RequestFormForm()
    
    return render(request, 'create_request.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RequestForm
from django.contrib.auth.models import User

@login_required
def list_request(request):
    user = request.user

    # If the user is a Manager, show only pending requests for approval
    if user.has_perm('forms.can_approve_request'):
        requests = RequestForm.objects.filter(approval_status='pending')

    # If the user is a Supervisor, show approved requests that need to be checked
    elif user.has_perm('forms.can_review_supervisor'):
        requests = RequestForm.objects.filter(approval_status='approved', supervisor_status='pending')

    # If the user is an Engineer, show only requests assigned to them
    elif user.has_perm('forms.can_assign_engineer'):
        requests = RequestForm.objects.filter(assigned_engineer=user)

    # If the user is Staff, show their own requests (based on submitted_by or created_by)
    else:
        requests = RequestForm.objects.filter(submitted_by=user)  # Use 'submitted_by' to filter by user

    # Pass engineers to the template for the dropdown (for assigning engineers)
    engineers = User.objects.filter(groups__name='Engineers')

    return render(request, 'list_request.html', {'requests': requests, 'engineers': engineers})


@login_required
@permission_required('forms.can_approve_request', raise_exception=True)
def approve_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    req.approval_status = 'approved'
    req.approved_by = request.user
    req.approved_at = timezone.now()
    req.save()
    return redirect('forms:list_request')  # Redirect back to the list

@login_required
@permission_required('forms.can_reject_request', raise_exception=True)
def reject_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    req.approval_status = 'rejected'
    req.approved_by = request.user
    req.approved_at = timezone.now()
    req.save()
    return redirect('forms:list_request')  # Redirect back to the list

@login_required
@permission_required('forms.can_assign_engineer', raise_exception=True)
def assign_engineer(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    if request.user.has_perm('forms.can_assign_engineer') and req.approval_status == 'approved' and req.supervisor_status == 'approved' and not req.assigned_engineer:
        if request.method == 'POST':
            engineer_id = request.POST.get('engineer')
            engineer = User.objects.get(id=engineer_id)
            req.assigned_engineer = engineer
            req.save()
            return redirect('forms:list_request')  # Redirect back to the request list

    return HttpResponseForbidden("You do not have permission to assign an engineer.")

@login_required
@permission_required('forms.can_check_request', raise_exception=True)
def check_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    req.approval_status = 'checked'
    req.checked_by = request.user
    req.checked_at = timezone.now()
    req.save()
    return redirect('forms:list_request')

@login_required
@permission_required('forms.can_review_supervisor', raise_exception=True)
def supervisor_review(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)

    if request.method == 'POST':
        form = SupervisorReviewForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect('forms:list_request')
    else:
        form = SupervisorReviewForm(instance=req)

    return render(request, 'supervisor_review.html', {'form': form, 'request_obj': req})













