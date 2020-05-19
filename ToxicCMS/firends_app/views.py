from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from firends_app.models import FriendsList
from userprofile.models import Profile


@login_required
def add_friend_request(request):
    if request.is_ajax():
        friend_to_add = Profile.objects.get(pk=request.POST.get("friendId"))
        if friend_to_add:
            friend_status = FriendsList.objects.filter(Q(person=request.user.profile) & Q(friend=friend_to_add))
            if not friend_status:
                friend_request = FriendsList.objects.create(
                    person=request.user.profile,
                    friend=friend_to_add,
                    status=1
                )
                mirrored_request = FriendsList.objects.create(
                    person=friend_to_add,
                    friend=request.user.profile,
                    status=2
                )

                return JsonResponse({'status': 1, 'message': 'friend request sent'})

    return JsonResponse({'status': 0, 'message': ''})


@login_required
def confirm_friend_request(request):
    if request.is_ajax():
        friend_to_accept = Profile.objects.get(pk=request.POST.get("friendId"))
        if friend_to_accept:
            try:
                friend_status = FriendsList.objects.get(
                    Q(person=request.user.profile) &
                    Q(friend=friend_to_accept) &
                    Q(status=2))
            except FriendsList.DoesNotExist:
                friend_status = None

            if friend_status:
                try:
                    mirrored_status = FriendsList.objects.get(
                        Q(person=friend_status.friend) &
                        Q(friend=friend_status.person) &
                        Q(status=1))
                except FriendsList.DoesNotExist:
                    mirrored_status = FriendsList.objects.create(
                        person=friend_status.friend,
                        friend=friend_status.person,
                        status=3
                    )
                mirrored_status.status = 3
                friend_status.status = 3
                friend_status.save()
                mirrored_status.save()
                return JsonResponse({'status': 1, 'message': 'friend request accepted'})

    return JsonResponse({'status': 0, 'message': ''})


@login_required
def remove_friend(request, pk):
    friend_to_remove = get_object_or_404(Profile, pk=pk)
    if request.method == 'GET':
        return render(request, 'firends_app/remove_friend.html', {'friend': friend_to_remove})
    else:
        try:
            friend_status = FriendsList.objects.get(
                Q(person=request.user.profile) &
                Q(friend=friend_to_remove) &
                Q(status=3))
        except FriendsList.DoesNotExist:
            return redirect('feed_news')

        mirrored_status = FriendsList.objects.get(
                Q(person=friend_to_remove) &
                Q(friend=request.user.profile) &
                Q(status=3))
        friend_status.delete()
        mirrored_status.delete()
        return redirect('feed_news')


@login_required
def friends_list(request):
    try:
        friends = sorted(list(FriendsList.objects.filter(person=request.user.profile)), key=lambda x: x.person.user.username)
    except FriendsList.DoesNotExist:
        friends = []

    return render(request, 'firends_app/friends_list.html', {'friends': friends})
