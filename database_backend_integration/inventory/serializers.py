from rest_framework import serializers
from .models import Ready  # Replace with actual model

class ReadySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ready
        fields = '__all__'  # Include all columns
