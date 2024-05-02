from rest_framework import serializers

from ..models import Computer

class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = ('id', 'name', 'status', 'created_at')
        extra_kwargs = {
            'status': {'read_only': True}, 
            'created_at': {'read_only': True}, 
        }

class ComputerStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = ('status', )