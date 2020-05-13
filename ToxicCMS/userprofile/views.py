from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.views import AuthenticationForm
from userprofile.forms import UserProfileForm
from userprofile.models import Profile


class UserLogin(FormView):
    template_name = 'userprofile/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is None:
            context = dict(form=form,
                           error_message='Invalid Credentials!')
            return self.render_to_response(context)
        else:
            login(self.request, user)
            return redirect('feed_news')


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('user_login')


def user_register(request):
    if request.method == 'GET':
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
        return render(request, 'userprofile/register.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        user.save()
        profile_form = UserProfileForm(request.POST, instance=user.profile)
        profile_form.save()
        login(request, user)
        return redirect('feed_news')


def find_profile(request):
    if request.is_ajax():
        profile_data = []
        search_value = request.GET.get("search_value")
        if search_value != '':
            profiles = Profile.objects.filter(user__username__icontains=search_value)
            friends = list(request.user.profile.friends.all())
            for profile in profiles:
                is_friend = False
                if profile in friends:
                    is_friend = True
                profile_data.append({"username": profile.user.username, "profileId": profile.id, "isFriend": is_friend})

        return JsonResponse(data=profile_data, safe=False)


def show_profile(request, pk):
    return render(request, 'userprofile/show_profile.html')


def edit_profile(request):
    pass


def show_friends(request):
    pass


@login_required
def test_view(request):
    return render(request, 'userprofile/edit_profile.html')
