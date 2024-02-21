from django.urls import path
from .views import PollRoomList, PollOptionList, create_poll_room, vote_poll_option,PollRoomData

urlpatterns = [
    path('poll-rooms/', PollRoomList.as_view(), name='poll-room-list-create'),
    path('poll-options/', PollOptionList.as_view(), name='poll-option-list-create'),
    # poll-options un varlığına neden onay verdiğimi hala bilmiyorum
    path('poll-rooms/<int:pr>', PollRoomData, name='poll-room'),# getting room and polls
    path('create-poll-room/', create_poll_room, name='create-poll-room'),
    path('vote-poll-option/', vote_poll_option, name='vote-poll-option'),
]


