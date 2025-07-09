class UnfinishedWarning(Warning):
    def __init__(self,text=None):
        super().__init__(text)