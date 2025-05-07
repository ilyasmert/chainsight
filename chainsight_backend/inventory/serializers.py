from rest_framework import serializers
from .models import Ready, AtpStock, Intransit, ToBeProduced, Sales, Users, ReadyArchive, AtpStockArchive, IntransitArchive, ToBeProducedArchive, SalesArchive
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

class ReadyArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyArchive
        fields = '__all__'  # Include all columns

class AtpStockArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtpStockArchive
        fields = '__all__'  # Include all columns

class IntransitArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntransitArchive
        fields = '__all__'  # Include all columns

class ToBeProducedArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToBeProducedArchive
        fields = '__all__'  # Include all columns

class SalesArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesArchive
        fields = '__all__'  # Include all columns

