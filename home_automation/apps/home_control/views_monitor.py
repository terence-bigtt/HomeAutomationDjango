# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, HttpResponse
from .models import MenuItem, IpCamDevice
from .device.ipcamdevice import IpCamFactory

menu = MenuItem.objects.order_by('id')

cams = [IpCamFactory(c).get() for c in IpCamDevice.objects.all()]


def get_cam_or_404(cam_id):
    cam_model = get_object_or_404(IpCamDevice, id=cam_id)
    selected_cam = IpCamFactory(cam_model).get()
    return selected_cam


def monitor(request, cam_id=None):
    selected_cams = cams
    ncol = request.GET.get("column")
    if ncol is None:
        ncol = 1
    ncol = int(ncol)
    if cam_id is not None:
        cam_db = IpCamDevice.objects.get(id=cam_id)
        selected_cams = [IpCamFactory(cam_db).get()]

    context = {"cams": selected_cams}
    return render(request, "home_control/cam.html", context)


def cam_ctrl(request, cam_id, ctrl):
    selected_cam = get_cam_or_404(cam_id)
    cmd = selected_cam.run_control(ctrl)
    if cmd is not None:
        return HttpResponse(cmd)
    return HttpResponse(status=405)

def feed(request, cam_id):
    selected_cam = get_cam_or_404(cam_id)
    selected_cam.playing = True
    return StreamingHttpResponse(selected_cam.stream(), content_type="multipart/x-mixed-replace; boundary=frame")


def preview(request, cam_id):
    selected_cam = get_cam_or_404(cam_id)
    return HttpResponse(selected_cam.run(), content_type='image/jpeg')


def links(request):
    context = {"menu": menu, "links": []}
    return render(request, "home_control/links.html", context)
