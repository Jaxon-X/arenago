from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StartRegistrationSerializer, VerifyRegistrationSerializer

class StartRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StartRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_data = serializer.save()

        return Response({
            'status': True,
            'phone_number': validate_data.get('phone_number'),
            'otp_code': validate_data.get('otp_code'),
        }, status=status.HTTP_200_OK)


class VerifyRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        response_data = {
            "user_id": user.id,
            "phone_number": user.phone_number,
            "role": user.role,
            "access": serializer.validated_data.get('access'),
            "refresh": serializer.validated_data.get('refresh'),
        }
        return Response(response_data, status=status.HTTP_200_OK)




