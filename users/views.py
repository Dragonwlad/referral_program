import time
from secrets import token_urlsafe

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAdminUser)
from rest_framework.response import Response
from rest_framework.views import APIView
from smsru.service import SmsRuApi
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .serializers import (UserCreateSerializer,
                          UserProfileSerializer)


def get_confirmation_code():
    '''Генерация 4х значного токена.'''
    return token_urlsafe(3)


def send_confirmation_code(phone_number, confirmation_code):
    '''Отправка СМС. Иммитация.'''
    message = f'Код авторизации: {confirmation_code}'
    sms_api = SmsRuApi()
    sms = sms_api.send_one_sms(phone=str(phone_number), msg=message)
    # Заглушка отправки смс
    print('------------------', sms)
    print('------------------', message)
    time.sleep(1)


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def create_user(request):
    """Регистрация пользователя."""
    serializer = UserCreateSerializer(data=request.data)
    phone_number = request.data.get('phone_number')

    if User.objects.filter(phone_number=phone_number):
        user = User.objects.get(phone_number=request.data['phone_number'])
        send_confirmation_code(
            phone_number=user.phone_number,
            confirmation_code=user.confirmation_code
        )
        return Response(
            {'message': 'Пользователь c таким номером уже существует. '
             'Код подтверждения отправлен повторно .'
             },
            status=status.HTTP_200_OK
        )

    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(phone_number=phone_number)
    confirmation_code = get_confirmation_code()
    serializer.save(
        confirmation_code=confirmation_code
    )
    phone_number = request.data.get('phone_number')
    send_confirmation_code(phone_number, confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def create_token(request):
    '''Получение токена по коду из СМС.'''
    phone_number = request.data.get('phone_number', None)
    confirmation_code = request.data.get('confirmation_code', None)
    if not phone_number:
        return Response(
            {'phone_number': 'Обязательное поле.'},
            status=status.HTTP_400_BAD_REQUEST)
    if not confirmation_code:
        return Response(
            {'confirmation_code': 'Обязательное поле.'},
            status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, phone_number=phone_number)
    correct_confirmation_code = user.confirmation_code
    if confirmation_code == correct_confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_201_CREATED)
    else:
        return Response('Неверный confirmation_code',
                        status=status.HTTP_400_BAD_REQUEST)


class UserProfileGetPath(APIView):
    '''Класс для просмотра и редактирования своего реферального профиля.'''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Получить информацию о своем профиле.'''
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        '''Внести inviter_code.'''
        user = request.user
        if user.inviter_code:
            return Response(
                {'inviter_code': 'Вы уже ввели инвайт-код пригласившего '
                 'вас пользователя.'},
                status=status.HTTP_403_FORBIDDEN)
        inviter_code = request.data.get('inviter_code', None)
        serializer = UserProfileSerializer(user,
                                           data=request.data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        if inviter_code == user.my_invite_code:
            return Response(
                {'inviter_code': 'Нельзя вводить свой инвайт-код.'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return self.get(request)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminUser,)
