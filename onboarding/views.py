from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage, OnboardingText, Complaint
from .serializers import ChatMessageSerializer, OnboardingTextSerializer, \
    ComplaintSerializer


class OnboardingTextAPIView(APIView):
    def get(self, request):
        queryset = OnboardingText.objects.all()
        serializer = OnboardingTextSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OnboardingTextSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnboardingTextDetailView(APIView):
    def get_object(self, pk):
        try:
            return OnboardingText.objects.get(pk=pk)
        except OnboardingText.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        onboarding_text = self.get_object(pk)
        serializer = OnboardingTextSerializer(onboarding_text)
        return Response(serializer.data)

    def put(self, request, pk):
        onboarding_text = self.get_object(pk)
        serializer = OnboardingTextSerializer(onboarding_text,
                                              data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        onboarding_text = self.get_object(pk)
        onboarding_text.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatMessageView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]


class ComplaintView(generics.ListCreateAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
