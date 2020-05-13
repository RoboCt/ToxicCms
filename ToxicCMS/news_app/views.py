from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from news_app.forms import EditFeedForm
from news_app.models import Feed


@login_required
def feed_news(request, username=''):
    new_feed_form = EditFeedForm()
    if username == '':
        friends = [val for val in request.user.profile.friends.all()] + [request.user.profile]
        feeds = Feed.objects.filter(author__profile__in=friends).order_by('-date_created')
    else:
        feeds = Feed.objects.filter(author__username=username).order_by('-date_created')

    return render(request, 'news_app/news_feed.html', {"feeds": feeds, "new_feed_form": new_feed_form})


@login_required
def create_feed(request):
    if request.method == 'POST':
        new_feed = Feed.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            author=request.user)
        new_feed.save()

        return render(request, 'news_app/feed.html',
                      {'feed_id': new_feed.id,
                       'title': new_feed.title,
                       'content': new_feed.content,
                       'author': new_feed.author,
                       'date_created': new_feed.date_created})


@login_required
def edit_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk, author=request.user)
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
    feed = get_object_or_404(Feed, pk=pk, author=request.user)
    if request.method == 'GET':
        return render(request, 'news_app/delete_feed.html', {'feed': feed,})
    if request.method == 'POST':
        feed.delete()
        return redirect('feed_news')

