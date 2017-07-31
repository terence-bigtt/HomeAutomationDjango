from .device import Device


class WebCam(Device) :
    def __init__(self, name, location= None):
        Device.__init__(self,name, "webcam", location)
