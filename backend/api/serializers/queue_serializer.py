from rest_framework import serializers
from string import ascii_uppercase

from ..models import Queue

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('id', 'account', 'computer', 'number', 'status', 'created_at')
        extra_kwargs = {
            'computer': {'read_only': True},
            'number': {'read_only': True}, 
            'status': {'read_only': True}, 
            'created_at': {'read_only': True}, 
        }

    def create(self, validated_data):
        # Generate a queue number for queue data Ex. A01, B02
        # Get the Last Queue
        last_queue = Queue.objects.order_by('-created_at').first()

        # Check if last queue is there
        if last_queue:
            last_alpha = ''.join(filter(str.isalpha, last_queue.number))
            last_num = ''.join(filter(str.isdigit, last_queue.number))
            new_num = int(last_num) + 1
            if new_num > 99:
                new_num = 1
                last_alpha_index = ascii_uppercase.index(last_alpha)
                new_alpha = ascii_uppercase[(last_alpha_index + 1) % len(ascii_uppercase)]
            else:
                new_alpha = last_alpha
            validated_data['number'] = new_alpha + str(new_num).zfill(2)
        else:
            validated_data['number'] = 'A01'

        return super().create(validated_data)


class QueueStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('status',)