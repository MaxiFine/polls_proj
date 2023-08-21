from django.urls import path
from .views import (HomePageView, AboutPageView,
                    PollsCreateView, PollsListView, 
                    PollDetailView, EditPollView, share_poll,
                     vote, results,)




urlpatterns = [
    # Pages urls
    path('', HomePageView.as_view(), name='home'),
    path('', AboutPageView.as_view(), name='about'),
    # Editing urls
    path('create-poll/', PollsCreateView.as_view(), name='create_poll'),
    path("<int:pk>/share-poll/", share_poll, name='share_poll'),
    path('list-poll', PollsListView.as_view(), name='list_poll'),
    path('polls-detail/<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('edit-poll/<int:pk>/', EditPollView.as_view(), name='edit_poll'),
    # Voting
    path('vote/<int:pk>/', vote, name='vote'),
    path('poll-results/<int:poll_id>/', results, name='poll_results'),
]