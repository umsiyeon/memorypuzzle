class failcount:
    def __init__(self):
        self.result = 0

    def count(self, click):
        self.result += click

    def total(self):
        return self.result

player = failcount()
