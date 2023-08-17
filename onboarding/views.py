from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OnboardingText
from .serializers import OnboardingTextSerializer


class OnboardingTextView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Получение текста для обучения в порядке отображения.

        Parameters:
            last_ordered_text_id (int): Идентификатор последнего выведенного текста.
                                       Если None, вернется первый текст в порядке.

        Returns:
            serialized_text (dict): Сериализованный объект текста для обучения.

        Example:
            /api/onboarding/text/?last_ordered_text_id=1
        """
        last_ordered_text_id = request.query_params.get('last_ordered_text_id',
                                                        None)

        if last_ordered_text_id is None:
            text = OnboardingText.objects.order_by('order').first()
        else:
            try:
                current_text = OnboardingText.objects.get(
                    pk=last_ordered_text_id)
                text = OnboardingText.objects.filter(
                    order__gt=current_text.order).order_by('order').first()
            except OnboardingText.DoesNotExist:
                text = None

        serializer = OnboardingTextSerializer(text)
        return Response(serializer.data, status=status.HTTP_200_OK)
