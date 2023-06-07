from web.video_camera import VideoCamera
from web.models import Cam


class CamCache():
    def __init__(self) -> None:
        self.cache = dict()
        ### Start cache
        for cam_instance in Cam.objects.all():
            print(str(cam_instance.id))
            self.add(cam_instance)

    def add(self, cam_instance):
        self.cache[cam_instance.id] = VideoCamera(cam_instance)
        print(self.cache)

    def delete(self, cam_id):
        cam = self.cache.pop(cam_id, None)
        cam.live = False
        del (cam)

    def get(self, cam_id):
        return self.cache[cam_id]


cam_cache = CamCache()