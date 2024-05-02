from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

Account = get_user_model()

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username')

class AccountUpdatePasswordSerializer(serializers.ModelSerializer):
    old_passwod = serializers.CharField(write_only=True)
    new_passwod = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('old_password', 'new_password')

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if not check_password(old_password, user.password):
            raise serializers.ValidationError({'detail': 'Incorrect old password.'})
        
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance