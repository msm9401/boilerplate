from django.contrib.auth import get_user_model, login, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegister(APIView):
    """
    - 회원가입
    """

    # @swagger_auto_schema(
    #     tags=["회원가입"],
    #     request_body=UserRegisterSerializer,
    #     query_serializer=UserRegisterSerializer,
    # )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = TokenObtainPairSerializer.get_token(user)
        return Response(
            {
                "user": serializer.data,
                "access_token": str(token.access_token),
                "refresh_token": str(token),
            },
            status=status.HTTP_200_OK,
        )


class UserLogin(APIView):
    """
    - 로그인
    """

    # @swagger_auto_schema(
    #     tags=["로그인"],
    #     request_body=UserLoginSerializer,
    #     query_serializer=UserLoginSerializer,
    # )
    def post(self, request):
        token_serializer = TokenObtainPairSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        user = token_serializer.user
        serializer = UserLoginSerializer(user)
        return Response(
            {
                "user": serializer.data,
                "access_token": token_serializer.validated_data.get("access"),
                "refresh_token": token_serializer.validated_data.get("refresh"),
            },
            status=status.HTTP_200_OK,
        )


# class UserRegister(APIView):

#     """회원 가입"""

#     # 기본 세션 회원 가입
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         serializer = UserRegisterSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class UserLogin(APIView):

#     """로그인"""

#     # 기본 세션 로그인
#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")
#         if not email or not password:
#             return Response(
#                 {"error": "something wrong!"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         user = authenticate(request, email=email, password=password)
#         if user is None:
#             return Response(
#                 {"error": "something wrong!"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         login(request, user)
#         return Response({"ok": "welcome!"}, status=status.HTTP_200_OK)
