from django.forms import ModelForm
from news_app.models import Feed


class EditFeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ['title', 'content']

