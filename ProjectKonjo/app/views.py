"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest, StreamingHttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import AddBluetoothDeviceForm
from .models import BluetoothDevice
from . import btservice
import bluetooth
from django.contrib.auth.models import User

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    assert isinstance(request.user, User)

    return render(request, 'app/index.html', { 'title':'Home Page', 'year' :datetime.now().year,'amount_approved_bluetooth_devices':len(BluetoothDevice.objects.all()), 'amount_detected_bluetooth_devices':len(btservice.all_detected_devices), 'last_login': request.user.last_login.date() })

@login_required
def bluetooth_page(request):
    assert isinstance(request, HttpRequest)
    bluetoothdevices = BluetoothDevice.objects.all()
    

    print(len(btservice.known_detected_devices))

    return render(request, 'app/bluetooth.html', {'bluetoothdevices':bluetoothdevices, 'detecteddevices':btservice.known_detected_devices})

@login_required
def add_bluetooth_device(request):
    assert isinstance(request, HttpRequest)
    print("Add bluetooth device")

    if(request.method == "GET"):
        if(request.GET.get('a', '') is not '' and request.GET.get('n', '') is not ''):
           addr = request.GET.get('a')
           name = request.GET.get('n')

           bluetoothdevice = BluetoothDevice()
           bluetoothdevice.bluetoothaddress = addr;
           bluetoothdevice.displayname = name;
           bluetoothdevice.save()

           return redirect("/bluetooth")

        form = AddBluetoothDeviceForm()
        bluetoothdevices = BluetoothDevice.objects.all()
        nearby_devices = btservice.all_detected_devices

        for dev in nearby_devices[:]:
                for device in bluetoothdevices:
                    if device.bluetoothaddress == dev.bluetoothaddress:
                        nearby_devices.remove(dev)
            
        return render(request, 'app/bluetooth/add.html', {'form':form, 'nearby_devices':nearby_devices})

    if(request.method == "POST"):
        addbluetoothdevice_form = AddBluetoothDeviceForm(request.POST)

        if(addbluetoothdevice_form.is_valid()):
            print("Adding: " + addbluetoothdevice_form.cleaned_data['bluetoothaddress'])

            bluetoothdevice = BluetoothDevice()
            bluetoothdevice.bluetoothaddress = addbluetoothdevice_form.cleaned_data['bluetoothaddress']
            bluetoothdevice.displayname = addbluetoothdevice_form.cleaned_data['displayname']
            bluetoothdevice.save()
        
        
    return redirect("/bluetooth")

@login_required
def remove_bluetooth_device(request):
    assert isinstance(request, HttpRequest)
    print("Remove bluetooth device")

    if(request.method == "GET"):
        btaddress = request.GET.get('a', '')
        bluetoothdevice = BluetoothDevice.objects.get(bluetoothaddress = btaddress)
        bluetoothdevice.delete()

    return redirect("/bluetooth")
