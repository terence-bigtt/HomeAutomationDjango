import base64
import uuid
import requests
from .device import Device
import time


class IpCamFactory(object):
    def __init__(self, ip_cam_model):
        self.ipcam_model = ip_cam_model

    def get(self):
        model = self.ipcam_model
        return IpCamDevice(model.name, model.location, model.id, model.ip, model.cam_user, model.cam_password,
                           model.capture_path,
                           model.payload, model.authentication, model.cam_ctrl)


class IpCamDevice(Device):
    def __init__(self, name, location, device_id=uuid.uuid4(), ip=None, cam_user=None, cam_password=None,
                 capture_path=None, payload=None, authentication=None, cam_ctrl=None):
        """
        Driver for IpCam type devices.
        :param name: name of the device
        :param location: physical location
        :param device_id: unique identifier for the device
        :param ip: ip on the network
        :param cam_user: user name for accessing the cam
        :param cam_password: password for accessing the cam
        :param capture_path: address to call for getting a snapshot
        :param payload parameters to pass to the capture url
        :param authentication : type of authentication
        :param cam_ctrl: dict of name -> route such that ip/route is called for actions on cam
        """
        Device.__init__(self, name, "ipcam", location, device_id)
        self.ip = ip
        self.cam_user = cam_user
        self.cam_password = cam_password
        self.capture_path = capture_path
        self.payload = payload
        self.authentication = authentication
        self.cam_ctrl = cam_ctrl
        self.cam_ctrl_keys = []
        if cam_ctrl is not None:
            self.cam_ctrl_keys = self.cam_ctrl.keys()
        self.playing = False

    def _auth_header(self):
        if self.authentication == "BASIC":
            auth_string = (self.cam_user + ":" + self.cam_password).encode("utf-8")
            b64_auth = base64.standard_b64encode(bytes(auth_string)).decode('utf-8')
            return {"Authorization": "BASIC " + b64_auth}

    def _http_parameters(self):
        headers = None
        if self.authentication is not None:
            headers = self._auth_header()

        params = {"headers": headers}
        params = {k: params.get(k) for k in params.keys() if params.get(k) is not None}
        return params

    def _make_url(self, path):
        return "http://" + self.ip + "/" + path

    def _request(self, path):
        capture_url = self._make_url(path)
        params = self._http_parameters()
        req = requests.get(capture_url, params=self.payload, **params)
        return req

    def run(self):
        req = self._request(self.capture_path)
        return req.content

    def run_control(self, name):
        if self.cam_ctrl is not None:
            path = self.cam_ctrl.get(name)
            req = self._request(path)
            return req.content


    def stream(self, fps=1):
        self.playing = True
        while self.playing:
            start = time.time()
            frame = self.run()
            frame_delay = time.time() - start
            wait_time = max(1/float(fps) - frame_delay,0)
            time.sleep(wait_time)
#            yield frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
