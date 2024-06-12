from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RequestGetRpgDashboardSerializer, RpgDashboardSerializer
from rpg_dashboard_service_app.models import RpgDashboard
from django.db import transaction
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncYear, TruncMonth
import sys

class RpgDashboardViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('hotel_id', openapi.IN_QUERY, description="Hotel ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('period', openapi.IN_QUERY, description="Dashboard Period Date", type=openapi.TYPE_STRING),
            openapi.Parameter('year', openapi.IN_QUERY, description="Dashboard year of choice", type=openapi.TYPE_INTEGER),
            openapi.Parameter('month', openapi.IN_QUERY, description="Dashboard month of choice", type=openapi.TYPE_INTEGER),
            openapi.Parameter('day', openapi.IN_QUERY, description="Dashboard day of choice", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: 'Successfully Retrieved',
            400: 'Bad Request',
            500: 'Server Error'
        }
    )
    @action(detail=False, methods=['get'])
    def list_events(self, request):
        payload = RequestGetRpgDashboardSerializer(data=request.query_params)
        if not payload.is_valid():
            output = {'success': 'FAILED', 'data': None, 'message': payload.error_messages, 'error': payload.errors}
            return Response(output, status=status.HTTP_400_BAD_REQUEST)

        validated_payload = payload.validated_data
        try:
            rpg_dashboard = RpgDashboard.objects.filter()

            if validated_payload.get('hotel_id'):
                rpg_dashboard = rpg_dashboard.filter(hotel_id=validated_payload.get('hotel_id'))

            if validated_payload.get('year'):
                rpg_dashboard = rpg_dashboard.filter(period__year = validated_payload.get('year'))
            
            if validated_payload.get('month') and validated_payload.get('year'):
                rpg_dashboard = rpg_dashboard.filter(period__month = validated_payload.get('month'))

            if validated_payload.get('day') and validated_payload.get('month') and validated_payload.get('year'):
                rpg_dashboard = rpg_dashboard.filter(period__day = validated_payload.get('day'))
            elif validated_payload.get('day') and not (validated_payload.get('month') and validated_payload.get('year')):
                output = {'success': 'FAILED', 'data': None, 'message': 'Must input year and month first', 'error': None}
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
            
            rpg_dashboard = rpg_dashboard.order_by('period')

            if validated_payload.get('period') == 'year':
                data = rpg_dashboard.annotate(period_year=TruncYear('period')).values('period_year', 'number_of_bookings')
                result = {}
                for item in data:
                    year = item['period_year'].year
                    if year in result:
                        result[year] += item['number_of_bookings']
                    else:
                        result[year] = item['number_of_bookings']
                data_output = [{'period': year, 'number_of_bookings': bookings} for year, bookings in result.items()]
            elif validated_payload.get('period') == 'month':
                data = rpg_dashboard.annotate(period_month=TruncMonth('period')).values('period_month', 'number_of_bookings')
                result = {}
                for item in data:
                    month = item['period_month'].strftime('%Y-%m')
                    if month in result:
                        result[month] += item['number_of_bookings']
                    else:
                        result[month] = item['number_of_bookings']
                data_output = [{'period': month, 'number_of_bookings': bookings} for month, bookings in result.items()]
            elif validated_payload.get('period') == 'day':
                data = rpg_dashboard.values('period', 'number_of_bookings')
                data_output = [{'period': item['period'].strftime('%Y-%m-%d'), 'number_of_bookings': item['number_of_bookings']} for item in data]
            # data_output = RpgDashboardSerializer(rpg_dashboard, many=True).data
        
            output = {'success': 'SUCCESS', 'data': data_output, 'message': 'Successfully Retrieved', 'error': None}
            return Response(output, status=status.HTTP_200_OK)
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            error_message = "{}:{}".format(filename, line_number)

            output = {'success': 'ERROR', 'data': None, 'message': error_message, 'error': str(e)}
            return Response(output, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
