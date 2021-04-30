class TimeStampedState:
    def __init__(self, time_stamp, state):
        self.time_stamp = time_stamp
        self.state = state

    @staticmethod
    def from_toggleable_state_change(data_row):
        return TimeStampedState(data_row[4], data_row[3])
