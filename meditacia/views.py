from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Meditation
from .serializers import MeditationSerializer


@api_view(['GET', 'POST'])
def meditations_list(request):
    if request.method == 'GET':
        meditations = Meditation.objects.all()
        serializer = MeditationSerializer(meditations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MeditationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
