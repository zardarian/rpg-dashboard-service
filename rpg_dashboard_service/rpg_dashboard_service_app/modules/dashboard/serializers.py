from rest_framework import serializers
from rpg_dashboard_service_app.models import RpgDashboard

class RpgDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpgDashboard
        fields = '__all__'

class RequestGetRpgDashboardSerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField(required=True)
    period = serializers.ChoiceField(choices=['month', 'day', 'year'], required=True)
    year = serializers.IntegerField(required=True)
    month = serializers.IntegerField(required=False)
    day = serializers.IntegerField(required=False)
