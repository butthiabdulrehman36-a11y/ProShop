from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def login(request):
    """
    Authenticate an existing user and start a session.
    """

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username:
            return render(
                request,
                'accounts/login.html',
                {'error': 'Username is required.'},
            )

        if not password:
            return render(
                request,
                'accounts/login.html',
                {'error': 'Password is required.'},
            )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            auth_login(request, user)

            return redirect('/profile/')

        return render(
            request,
            'accounts/login.html',
            {'error': 'Invalid username or password.'},
        )

    return render(
        request,
        'accounts/login.html',
    )


@login_required(login_url='/login/')
def profile(request):
    """
    Display the logged-in user's profile page.
    """

    return render(
        request,
        'accounts/profile.html',
    )


def register(request):
    """
    Create a new customer account.
    """

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get(
            'confirm_password',
            '',
        )

        if not username:
            return render(
                request,
                'accounts/register.html',
                {'error': 'Username is required.'},
            )

        if not email:
            return render(
                request,
                'accounts/register.html',
                {'error': 'Email is required.'},
            )

        if not password:
            return render(
                request,
                'accounts/register.html',
                {'error': 'Password is required.'},
            )

        if not confirm_password:
            return render(
                request,
                'accounts/register.html',
                {'error': 'Confirm password is required.'},
            )

        if len(password) < 8:
            return render(
                request,
                'accounts/register.html',
                {
                    'error': (
                        'Password must be at least 8 characters long.'
                    )
                },
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'accounts/register.html',
                {'error': 'Username already exists.'},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                'accounts/register.html',
                {'error': 'Email already exists.'},
            )

        if password != confirm_password:
            return render(
                request,
                'accounts/register.html',
                {'error': 'Passwords do not match.'},
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        return redirect('/login/')

    return render(
        request,
        'accounts/register.html',
    )


def logout(request):
    """
    Log out the current user and return to the login page.
    """

    auth_logout(request)

    return redirect('/login/')