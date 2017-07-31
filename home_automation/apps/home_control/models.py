# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField


class IpCamDevice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=50, blank=True, default='')
    device_type = models.CharField(max_length=20, choices=(("ipcam", "Ip Cam",),), default="ipcam")
    ip = models.GenericIPAddressField()
    cam_user = models.CharField(max_length=20, blank=True, default='')
    cam_password = models.CharField(max_length=50, blank=True, default='')
    capture_path = models.CharField(max_length=200)
    payload = JSONField(blank=True, default="{}")
    authentication = models.CharField(max_length=20, choices=(("", "No Auth"), ("BASIC", "Basic Authentication")), default="", blank=True)
    cam_ctrl = JSONField(blank=True, default="{}")


class MenuItem(models.Model):
    caption = models.CharField(max_length=20)
    page = models.CharField(max_length=20)
    target = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)
