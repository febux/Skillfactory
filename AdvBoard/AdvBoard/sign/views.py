import string

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django.views.generic import View
from .models import BasicSignupForm, OneTimeCode
from posts.models import Author

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BasicSignupForm
    success_url = '/'


class VerCodeView(View):
    template_name = 'sign/ver_code_entering.html'


def random_ver_code(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.verification_code = random_ver_code()
            print(user.verification_code)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('sign/code_auth.html', {
                'user': user,
                'domain': current_site.domain,
                'ver_code': user.verification_code,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('/sign/ver_code_entering/')
    else:
        form = SignupForm()
    return render(request, 'sign/signup.html', {'form': form})


def activate(request, uidb64, code):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(user.verification_code)
    if user is not None and user.verification_code == code:
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    Author.objects.create(author=user)
    return redirect('/')

# def usual_login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         one_time_code = OneTimeCode.objects.create(code=random.choice('abcde'), user=user)
#         print(one_time_code)
#         # send e-mail with code
#
#     else:
#         pass


# def login_with_code_view(request):
#     username = request.POST['username']
#     code = request.POST['code']
#     if OneTimeCode.objects.filter(code=code, user__username=username).exists():
#         login(request, user)
#     else:
#         pass
