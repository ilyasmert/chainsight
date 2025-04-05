from rest_framework import serializers
from .models import Ready, AtpStock, Intransit, ToBeProduced, Sales, Users  # Replace with actual model

class ReadySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ready
        fields = '__all__'  # Include all columns

class AtpStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtpStock
        fields = '__all__'

class IntransitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intransit
        fields = '__all__'

class ToBeProducedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToBeProduced
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'