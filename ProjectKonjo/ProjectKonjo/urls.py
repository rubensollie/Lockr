"""
Definition of urls for ProjectKonjo.
"""

from datetime import datetime
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from django.conf.urls import url, include
from django.contrib.auth.models import User
import django.contrib.auth.views
from django.views.decorators.http import require_http_methods

from app.models import BluetoothDevice
from app import btservice

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BluetoothDevicesSerializer(serializers.Serializer):
    bluetoothaddress = serializers.CharField(max_length=17)
    displayname = serializers.CharField(max_length=40)

class KnownDetectedBluetoothDevicesViewSet (viewsets.ViewSet):
    serializer_class = BluetoothDevicesSerializer
    
    def list(self, request):
        serializer = BluetoothDevicesSerializer(instance = btservice.known_detected_devices, many=True)
        return Response(serializer.data)

class AllDetectedBluetoothDevicesViewSet (viewsets.ViewSet):
    serializer_class = BluetoothDevicesSerializer

    def list(self, request):
        serializer = BluetoothDevicesSerializer(instance = btservice.all_detected_devices, many=True)
        return Response(serializer.data)

class ApprovedBluetoothDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BluetoothDevice
        fields = ('url', 'bluetoothaddress', 'displayname')

class ApprovedBluetoothDevicesViewSet(viewsets.ModelViewSet):
    queryset = BluetoothDevice.objects.all()
    serializer_class = ApprovedBluetoothDevicesSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bluetooth/detected', KnownDetectedBluetoothDevicesViewSet, 'detected_devices')
router.register(r'bluetooth/all', AllDetectedBluetoothDevicesViewSet, 'all_devices')
router.register(r'bluetooth/approved', ApprovedBluetoothDevicesViewSet)

urlpatterns = [
    # Examples:
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),



    url(r'^$', app.views.home, name='home'),
    url(r'^bluetooth/approved$', app.views.bluetooth_page, name='bluetooth'),
    url(r'^bluetooth/detected/$', app.views.add_bluetooth_device, name='add_bluetooth_device'),
    url(r'^bluetooth/remove/$', app.views.remove_bluetooth_device, name='remove_bluetooth_device'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
