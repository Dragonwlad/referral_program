from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('phone_number',)
        model = User
        read_only_fields = ('confirmation_code', 'my_invite_code')


class UserProfileSerializer(serializers.ModelSerializer):
    numbers_of_invitees = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('my_invite_code', 'numbers_of_invitees', 'inviter_code')
        read_only_fields = ('my_invite_code', 'numbers_of_invitees')

    def get_numbers_of_invitees(self, obj):
        users_of_invitees = User.objects.filter(
            inviter_code=obj.my_invite_code)
        numbers_of_invitees = [str(user) for user in users_of_invitees]
        return numbers_of_invitees

    def validate_inviter_code(self, inviter_code):
        inviter = User.objects.filter(my_invite_code=inviter_code)

        if not inviter:
            raise serializers.ValidationError(
                'Пользователь с таким инвайт-кодом не найден.')
        return inviter_code
