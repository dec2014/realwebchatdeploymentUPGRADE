from rest_framework import serializers
from chat.models import Room,Messages

class roomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Room
        fields='__all__'
        read_only_fields=('room_name','created_by',)
    
    
    