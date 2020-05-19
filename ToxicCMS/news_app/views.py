from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from firends_app.models import FriendsList
from news_app.forms import EditFeedForm
from news_app.models import Feed
from userprofile.models import Profile


@login_required
def feed_news(request, username=''):
    new_feed_form = EditFeedForm()
    friendship = None
    if username == '':
        friend_relations = FriendsList.objects.filter(
            Q(person=request.user.profile) &
            Q(status=3))
        friends = [val.friend for val in friend_relations] + [request.user.profile]
        feeds = Feed.objects.filter(author__in=friends).order_by('-date_created')
        new_feed_visible = True
        author = None
    else:
        if username == request.user.username:
            feeds = Feed.objects.filter(author=request.user.profile).order_by('-date_created')
            new_feed_visible = True
            author = request.user.profile
        else:
            feeds = Feed.objects.filter(author__user__username=username).order_by('-date_created')
            new_feed_visible = False
            author = Profile.objects.get(user__username=username)
            try:
                friendship = FriendsList.objects.get(Q(person=request.user.profile) & Q(friend=author))
            except FriendsList.DoesNotExist:
                friendship = None

    return render(request, 'news_app/news_feed.html',
                  {
                      "feeds": feeds,
                      "new_feed_form": new_feed_form,
                      "new_feed_visible": new_feed_visible,
                      "author": author,
                      "friendship": friendship,
                  })


@login_required
def create_feed(request):
    if request.is_ajax():
        new_feed = Feed.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            author=request.user.profile)
        new_feed.save()

        return render(request, 'news_app/feed.html',
                      {'feed_id': new_feed.id,
                       'title': new_feed.title,
                       'content': new_feed.content,
                       'author': new_feed.author,
                       'date_created': new_feed.date_created})


@login_required
def edit_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk, author=request.user.profile)
    if request.method == 'GET':
        form = EditFeedForm(instance=feed)
        return render(request, 'news_app/edit_feed.html', {'feed': feed, 'form': form})
    else:
        try:
            form = EditFeedForm(request.POST, instance=feed)
            form.save()
            return redirect('feed_news')
        except ValueError:
            return render(request, 'news_app/edit_feed.html', {'feed': feed, 'form': form, 'error_message': 'wrong data'})


@login_required
def delete_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk, author=request.user.profile)
    if request.method == 'GET':
        return render(request, 'news_app/delete_feed.html', {'feed': feed,})
    if request.method == 'POST':
        feed.delete()
        return redirect('feed_news')

