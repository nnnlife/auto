from minerstate import state


class GoMiningStatus(state.State):
    def __init__(self, player):
        state.State.__init__(self, player)

    def on_event(self, event):
        return self
