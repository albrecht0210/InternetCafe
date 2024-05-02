from rest_framework import serializers

from ..models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'account', 'computer', 'start_time', 'end_time')
        extra_kwargs = {
            'start_time': {'read_only': True}
        }
        