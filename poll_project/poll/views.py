from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import PollRoom, PollOption
from .serializers import PollRoomSerializer, PollOptionSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class PollRoomList(generics.ListCreateAPIView):
    queryset = PollRoom.objects.all()
    serializer_class = PollRoomSerializer


class PollOptionList(generics.ListCreateAPIView):
    queryset = PollOption.objects.all()
    serializer_class = PollOptionSerializer


# poll_room/2 için mesela oda 2 nin seçeneklerini ve genel odanın bilgilerini görebilmek için
@api_view(['GET'])
@permission_classes([AllowAny])
def PollRoomData(request, pr) -> Response:
    room = get_object_or_404(PollRoom, id=pr)
    options = PollOption.objects.filter(poll_room=room)
    options_data = []
    for i in options:
        options_data.append({
            "id": i.id,
            "option_text": i.option_text,
            "vote_count": i.vote_count
        })
    response_data = {
        "room": {
            "id": room.id,
            "title": room.title
        },
        "options": options_data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def create_poll_room(request) -> Response:
    """
    requests:
    {
        "title":str
    }
    """
    if request.method == 'POST':
        serializer = PollRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        # GET isteği için bir şeyler yapmak istiyorsanız buraya yazabilirsiniz
        # Örneğin, tüm odaları listelemek gibi
        return Response("Only for POST requests.", status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def vote_poll_option(request) -> Response:
    """
    {
        room_id
        option_id
    }

    """
    data = request.data
    ip_address = request.META.get('REMOTE_ADDR')
    option_id = data["option_id"]
    room_id = data["room_id"]
    cache_opt = f"voted_ips_{option_id}"
    cache_room = f"already_voted_in_room_{room_id}"
    # İP Adresi kontrolü

    if cache.get(cache_opt):
        return Response({"error": "You have already voted for this option."}, status=400)

    if cache.get(cache_room):
        return Response({"error": "You have already voted for another option."}, status=404)

    try:
        poll_option = PollOption.objects.get(pk=option_id)
    except PollOption.DoesNotExist:
        return Response({"error": "Poll option does not exist."}, status=404)

    # IP adresini cache'e ekle (oy kullanıldığını işaretle)
    cache.set(cache_opt, True)
    cache.set(cache_room, True)

    poll_option.vote_count += 1
    poll_option.save()

    return Response({"message": "Vote added successfully."}, status=200)
