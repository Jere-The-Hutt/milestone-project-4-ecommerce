from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm, UserProfileForm
from .models import UserProfile
from orders.models import Order
from .tasks import send_account_deleted_email


@login_required
def profile_view(request):
    """Show the user's profile and order history."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    orders = Order.objects.filter(user=request.user).order_by('-created')

    context = {
        'user': request.user,
        'profile': profile,
        'orders': orders,
    }
    return render(request, 'user/profile.html', context)


@login_required
def profile_edit(request):
    """Let the user edit their profile and account info."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
            )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Your profile has been updated successfully!'
                )
            return redirect('account_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_edit.html', context)


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user_email = user.email

        send_account_deleted_email.delay(user_email)

        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('shop:product_list')

    return redirect('account_profile')
