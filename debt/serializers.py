from rest_framework import serializers
from .models import debt

class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = debt
        fields = '__all__'
        

