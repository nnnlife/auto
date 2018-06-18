import datetime


class Player:
    def __init__(self, mine_area):
        self.mine_area = mine_area
        self.try_count = 0
        self.mine_index = 0
        self.occupied_mine = []
        self.current_mine = None

    def get_mine_area(self):
        return self.mine_area[self.mine_index]

    def increase_try_count(self):
        self.try_count += 1
        print("TRY COUNT %d" % self.try_count)
        if self.try_count > 20:
            self.mine_index = (self.mine_index + 1) % len(self.mine_area)
            self.try_count = 0

    def decrease_try_count(self):
        self.try_count -= 1

    def get_try_count(self):
        return self.try_count

    def player_waiting_reset(self):
        self.try_count = 0
        self.mine_index = 0
        self.occupied_mine = []

    def base_area(self):
        return self.mine_area[0]

    def set_current_mine(self, pos):
        self.current_mine = pos

    def get_occupied_mine(self):
        new_occupied_mine = []
        for o in self.occupied_mine:
            if (datetime.datetime.now() - o[0]).total_seconds() < 60 * 60:
                new_occupied_mine.append(o)
        self.occupied_mine = new_occupied_mine
        return self.occupied_mine

    def add_occupied_mine(self):
        self.occupied_mine.append((datetime.datetime.now(), self.current_mine[0], self.current_mine[1]))