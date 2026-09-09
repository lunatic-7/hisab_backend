from rest_framework import serializers
from .models import Person, Hisab

class HisabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hisab
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    hisabs = HisabSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'hisabs']
