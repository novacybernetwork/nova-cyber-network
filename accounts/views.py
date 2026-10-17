from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator

from core.models import log_action
from core.utils import get_client_ip

from .forms import ClaimAccountForm, ProfileEditForm, RequestAccessForm, StyledAuthenticationForm
from .models import ApprovedMember, Profile, School


@method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True), name="post")
class RateLimitedLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm


@method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True), name="post")
class RateLimitedPasswordResetView(PasswordResetView):
    pass


def claim_invite(request, token):
    member = get_object_or_404(ApprovedMember, invite_token=token)

    if member.pending_review:
        return render(request, "accounts/claim_pending.html", {"member": member})
    if member.is_claimed:
        messages.info(request, "This invite has already been claimed. Please sign in instead.")
        return redirect("accounts:login")

    if request.method == "POST":
        form = ClaimAccountForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = member.email
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.display_name = member.name
            profile.school = member.school
            profile.approved_member = member
            profile.is_approved = True
            profile.save()
            member.mark_claimed(user)
            log_action(user, "account.claimed", target=member, ip_address=get_client_ip(request))
            login(request, user)
            messages.success(request, f"Welcome to NOVA Cyber Network, {member.name}!")
            return redirect("core:dashboard")
    else:
        form = ClaimAccountForm()

    return render(request, "accounts/claim.html", {"form": form, "member": member})


@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def request_access(request):
    if request.method == "POST":
        form = RequestAccessForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if ApprovedMember.objects.filter(email=email).exists():
                messages.info(request, "An invite already exists for that email. Check your inbox, or contact an administrator.")
                return redirect("accounts:request_access")

            school = form.cleaned_data["school"]
            if not school and form.cleaned_data.get("school_other"):
                school, _ = School.objects.get_or_create(name=form.cleaned_data["school_other"].strip())

            member = ApprovedMember.objects.create(
                name=form.cleaned_data["name"], email=email, school=school, pending_review=True
            )
            log_action(None, "membership.request_access", target=member, ip_address=get_client_ip(request))
            messages.success(request, "Your request has been submitted for administrator review.")
            return redirect("core:home")
    else:
        form = RequestAccessForm()
    return render(request, "accounts/request_access.html", {"form": form})


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, "accounts/profile.html", {"form": form})
