from rest_framework import serializers

from backend.models import costModel


class costSerializer(serializers.ModelSerializer):
    class Meta:
        model = costModel
        fields = [
            'id',
            'date',
            'expense',
            'amount',
            'reciept'

        ]
        depth = 1
