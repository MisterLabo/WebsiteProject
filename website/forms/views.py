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

def is_manager(user):
    return user.is_staff

def handle_invalid_request(req, user, action):
    logger.error(f"Invalid {action} attempt for request {req.id} by user {user.username}")
    messages.error(user, f"Request is not eligible for {action}.")
    return redirect('forms:list_request')

def get_requests_for_user(user):
    if user.has_perm('forms.can_approve_request'):
        return RequestForm.objects.filter(approval_status='pending')

    elif user.has_perm('forms.can_review_supervisor') and user.has_perm('forms.can_assign_engineer'):
        return RequestForm.objects.filter(
            approval_status='approved',
            supervisor_status__in=['pending', 'approved'],
            assigned_engineer__isnull=True
        )

    elif user.has_perm('forms.can_review_supervisor'):
        return RequestForm.objects.filter(
            approval_status='approved',
            supervisor_status='pending'
        )

    elif user.groups.filter(name='Engineers').exists():
        return RequestForm.objects.filter(assigned_engineer=user)

    else:
        return RequestForm.objects.filter(created_by=user)

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
            return redirect('forms:list_request')
        else:
            logger.warning(f"Invalid form submission by user {request.user.username}")
            messages.error(request, "Invalid form submission.")
    else:
        form = RequestFormForm()

    return render(request, 'create_request.html', {'form': form})

@login_required
def list_request(request):
    requests = get_requests_for_user(request.user)
    return render(request, 'list_request.html', {'requests': requests})

@login_required
@permission_required('forms.can_approve_request', raise_exception=True)
def approve_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    try:
        req.approve(request.user)
        logger.info(f"Request {req.id} approved by user {request.user.username}")
        messages.success(request, f"Request '{req.proposed_title}' approved successfully.")
    except ValueError as e:
        messages.error(request, str(e))
        logger.error(f"{str(e)} for request {req.id} by user {request.user.username}")
    return redirect('forms:list_request')

@login_required
@permission_required('forms.can_reject_request', raise_exception=True)
def reject_request(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    try:
        req.reject(request.user)
        logger.info(f"Request {req.id} rejected by user {request.user.username}")
        messages.success(request, f"Request '{req.proposed_title}' rejected successfully.")
    except ValueError as e:
        messages.error(request, str(e))
        logger.error(f"{str(e)} for request {req.id} by user {request.user.username}")
    return redirect('forms:list_request')

@login_required
@permission_required('forms.can_assign_engineer', raise_exception=True)
def assign_engineer(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    if request.method == 'POST':
        engineer_id = request.POST.get('engineer')
        try:
            engineer = User.objects.get(id=engineer_id)
            req.assign_engineer(engineer, request.user)
            logger.info(f"Engineer {engineer.username} assigned to request {req.id} by user {request.user.username}")
            messages.success(request, f"Engineer '{engineer.username}' assigned successfully.")
        except User.DoesNotExist:
            messages.error(request, "Invalid engineer ID.")
            logger.error(f"Invalid engineer ID {engineer_id} provided by user {request.user.username}")
        except ValueError as e:
            messages.error(request, str(e))
            logger.error(f"{str(e)} for request {req.id} by user {request.user.username}")
        return redirect('forms:list_request')

    engineers = User.objects.filter(groups__name='Engineers')
    return render(request, 'assign_request.html', {'request_obj': req, 'engineers': engineers})

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
@permission_required('forms.can_assign_engineer', raise_exception=True)
def supervisor_assign_engineer(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)

    logger.debug(f"Request ID: {req.id}, Approval Status: {req.approval_status}, Supervisor Status: {req.supervisor_status}")
    logger.debug(f"User: {request.user.username}, Permissions: {request.user.get_all_permissions()}")

    if request.method == 'POST':
        engineer_id = request.POST.get('engineer')
        try:
            engineer = User.objects.get(id=engineer_id)
            req.assign_engineer(engineer, request.user)
            logger.info(f"Engineer {engineer.username} assigned to request {req.id} by supervisor {request.user.username}")
            messages.success(request, f"Engineer {engineer.get_full_name()} assigned successfully.")
            return redirect('forms:list_request')
        except User.DoesNotExist:
            logger.error(f"Invalid engineer ID {engineer_id} provided by supervisor {request.user.username}")
            messages.error(request, "Invalid engineer selected.")
        except ValueError as e:
            messages.error(request, str(e))
            logger.error(f"{str(e)} for request {req.id} by supervisor {request.user.username}")
    else:
        engineers = User.objects.filter(groups__name='Engineers')
        return render(request, 'assign_request.html', {'request_obj': req, 'engineers': engineers})

@login_required
def request_detail(request, request_id):
    req = get_object_or_404(RequestForm, id=request_id)
    return render(request, 'request_detail.html', {'request': req})
