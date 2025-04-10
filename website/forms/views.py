import logging
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from .forms import RequestFormForm, SupervisorReviewForm
from .models import RequestForm
from django.http import HttpResponseForbidden

# Initialize logger
logger = logging.getLogger(__name__)

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
            logger.info(f"Request created by user {request.user.username} with ID {instance.id}")
            messages.success(request, "Request created successfully.")
            return redirect('forms:list_request')  # Or anywhere else
        else:
            logger.warning(f"Invalid form submission by user {request.user.username}")
            messages.error(request, "Invalid form submission.")
    else:
        form = RequestFormForm()
    
    return render(request, 'create_request.html', {'form': form})

@login_required
def list_request(request):
    user = request.user

    # Filter requests based on user permissions
    if user.has_perm('forms.can_approve_request'):
        requests = RequestForm.objects.filter(approval_status='pending')
    elif user.has_perm('forms.can_review_supervisor'):
        requests = RequestForm.objects.filter(approval_status='approved', supervisor_status='pending')
    elif user.has_perm('forms.can_assign_engineer'):
        requests = RequestForm.objects.filter(assigned_engineer=user)
    else:
        requests = RequestForm.objects.filter(submitted_by=user)

    # Pass engineers to the template for the dropdown (for assigning engineers)
    engineers = User.objects.filter(groups__name='Engineers')

    # Remove any references to `created_at` until the database schema is updated
    # Example: Do not sort or filter by `created_at`

    return render(request, 'list_request.html', {'requests': requests, 'engineers': engineers})

@login_required
@permission_required('forms.can_approve_request', raise_exception=True)
def approve_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    if req.approval_status != 'pending':
        messages.error(request, "Request is not in a pending state.")
        logger.error(f"Attempt to approve a non-pending request {req.id} by user {request.user.username}")
        return redirect('forms:list_request')
    req.approval_status = 'approved'
    req.approved_by = request.user
    req.approved_at = timezone.now()
    req.save()
    logger.info(f"Request {req.id} approved by user {request.user.username}")
    messages.success(request, f"Request '{req.proposed_title}' approved successfully.")
    return redirect('forms:list_request')

@login_required
@permission_required('forms.can_reject_request', raise_exception=True)
def reject_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    if req.approval_status != 'pending':
        messages.error(request, "Request is not in a pending state.")
        logger.error(f"Attempt to reject a non-pending request {req.id} by user {request.user.username}")
        return redirect('forms:list_request')
    req.approval_status = 'rejected'
    req.approved_by = request.user
    req.approved_at = timezone.now()
    req.save()
    logger.info(f"Request {req.id} rejected by user {request.user.username}")
    messages.success(request, f"Request '{req.proposed_title}' rejected successfully.")
    return redirect('forms:list_request')

@login_required
@permission_required('forms.can_assign_engineer', raise_exception=True)
def assign_engineer(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    if req.approval_status != 'approved' or req.supervisor_status != 'approved' or req.assigned_engineer:
        messages.error(request, "Request is not eligible for engineer assignment.")
        logger.error(f"Invalid engineer assignment attempt for request {req.id} by user {request.user.username}")
        return redirect('forms:list_request')
    if request.method == 'POST':
        engineer_id = request.POST.get('engineer')
        try:
            engineer = User.objects.get(id=engineer_id)
            req.assigned_engineer = engineer
            req.save()
            logger.info(f"Engineer {engineer.username} assigned to request {req.id} by user {request.user.username}")
            messages.success(request, f"Engineer '{engineer.username}' assigned successfully.")
            return redirect('forms:list_request')  # Redirect back to the request list
        except User.DoesNotExist:
            messages.error(request, "Invalid engineer ID.")
            logger.error(f"Invalid engineer ID {engineer_id} provided by user {request.user.username}")
            return redirect('forms:list_request')
    return HttpResponseForbidden("You do not have permission to assign an engineer.")

@login_required
@permission_required('forms.can_check_request', raise_exception=True)
def check_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    if req.approval_status != 'approved':
        messages.error(request, "Request is not in an approved state.")
        logger.error(f"Attempt to check a non-approved request {req.id} by user {request.user.username}")
        return redirect('forms:list_request')
    req.approval_status = 'checked'
    req.checked_by = request.user
    req.checked_at = timezone.now()
    req.save()
    logger.info(f"Request {req.id} checked by user {request.user.username}")
    messages.success(request, f"Request '{req.proposed_title}' checked successfully.")
    return redirect('forms:list_request')

@login_required
@permission_required('forms.can_review_supervisor', raise_exception=True)
def supervisor_review(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)

    if request.method == 'POST':
        form = SupervisorReviewForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            logger.info(f"Supervisor review completed for request {req.id} by user {request.user.username}")
            messages.success(request, f"Supervisor review completed for request '{req.proposed_title}'.")
            return redirect('forms:list_request')
        else:
            logger.warning(f"Invalid supervisor review form submission for request {req.id} by user {request.user.username}")
            messages.error(request, "Invalid supervisor review form submission.")
    else:
        form = SupervisorReviewForm(instance=req)

    return render(request, 'supervisor_review.html', {'form': form, 'request_obj': req})

@login_required
@permission_required('forms.can_review_supervisor', raise_exception=True)
def supervisor_assign_engineer(request, request_id):
    """
    Allows supervisors to assign engineers to approved requests.
    """
    req = get_object_or_404(RequestForm, id=request_id)

    # Ensure the request is approved and supervisor status is approved
    if req.approval_status != 'approved' or req.supervisor_status != 'approved':
        logger.error(f"Invalid assignment attempt for request {req.id} by supervisor {request.user.username}")
        raise PermissionDenied("Request must be approved by both manager and supervisor before assigning an engineer.")

    if request.method == 'POST':
        engineer_id = request.POST.get('engineer')
        try:
            engineer = User.objects.get(id=engineer_id)
            req.assigned_engineer = engineer
            req.assigned_at = timezone.now()
            req.save()
            logger.info(f"Engineer {engineer.username} assigned to request {req.id} by supervisor {request.user.username}")
            messages.success(request, f"Engineer {engineer.get_full_name()} assigned successfully.")
            return redirect('forms:list_request')
        except User.DoesNotExist:
            logger.error(f"Invalid engineer ID {engineer_id} provided by supervisor {request.user.username}")
            messages.error(request, "Invalid engineer selected.")
    else:
        engineers = User.objects.filter(groups__name='Engineers')
        return render(request, 'assign_request.html', {'request_obj': req, 'engineers': engineers})













