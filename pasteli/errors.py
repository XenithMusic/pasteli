class UnfinishedWarning(Warning):
    def __init__(self,text=None):
        super().__init__(text)

class ClipboardUtilityError(Exception):
    def __init__(self,text=None):
        super().__init__(text)

class ClipboardUtilityWarning(Warning):
    def __init__(self,text=None):
        super().__init__(text)