from scalekit_backend.scalekit_client import ScClient

class ScalekitUserService:
    def __init__(self):
        self.scalekit_client = ScClient()
        print("ScalekitUserService initialized")

    def get(self, scalekit_user_id):
        return self.scalekit_client.get_user_info(scalekit_user_id)
