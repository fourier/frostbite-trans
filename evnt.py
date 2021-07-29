class GetRoomDesc(object):
    def __init__(self, name = ""):
        self.name = name

class RequestTranslation(object):
    def __init__(self, text = ""):
        self.text = text

class SendTranslation(object):
    def __init__(self, original = "", translation = ""):
        self.original = original
        self.translation = translation


