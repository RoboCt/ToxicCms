from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth.views import AuthenticationForm
from firends_app.models import FriendsList
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
        profiles_data = []
        search_value = request.GET.get("search_value")
        if search_value != '':
            profiles = Profile.objects.filter(user__username__icontains=search_value)
            for profile in profiles:
                profiles_data.append({'id': profile.id, 'username': profile.user.username})

        return render(request, 'userprofile/profiles_found.html', {"profiles": profiles_data})


@login_required
def show_profile(request, pk):
    if request.user.profile.id == pk:
        friend_profile = request.user.profile
        friend_status = 99
    else:
        friend_profile = get_object_or_404(Profile, pk=pk)
        try:
            friend_request = FriendsList.objects.get(Q(person=request.user.profile) & Q(friend=friend_profile))
            friend_status = friend_request.status
        except FriendsList.DoesNotExist:
            friend_status = 0

    return render(request, 'userprofile/show_profile.html', {'profile': friend_profile, 'friendship_status': friend_status})


def edit_profile(request):
    pass


def show_friends(request):
    pass


@login_required
def test_view(request):
    return render(request, 'userprofile/edit_profile.html')
