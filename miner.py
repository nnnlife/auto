from minerstate import waitstatus, gomining


class Miner:
    def __init__(self, player, is_wait):
        self.player = player
        if is_wait:
            self.status = waitstatus.WaitStatus(player)
        else:
            self.status = gomining.GoMiningStatus(player)

    def is_waiting(self):
        return self.status.is_waiting()

    def next(self, event):
        self.status = self.status.on_event(event)

