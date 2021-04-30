from datetime import timedelta, datetime


class ToggleableOnTimeCalculator:
    @staticmethod
    def get_on_time(times, search_for_state, run_time=None):

        time_on = timedelta(minutes=0)
        last_found_time_stamp = None
        for data in times:
            if data.state == search_for_state and last_found_time_stamp is None:
                last_found_time_stamp = data.time_stamp
            elif last_found_time_stamp is not None and data.state != search_for_state:
                time_on = time_on + (data.time_stamp - last_found_time_stamp)
                last_found_time_stamp = None
            else:
                continue

        if run_time is None:
            run_time = datetime.now()

        last_time_stamped_state = times[len(times) - 1]
        if last_time_stamped_state.state == search_for_state:
            time_on += run_time - last_found_time_stamp

        return time_on
