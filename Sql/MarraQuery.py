insert_state_update = """
    INSERT INTO
        public.toggleable_status
            (toggleable_id, state)
        VALUES
            (%s, %s);
"""

insert_state_status = """
    INSERT INTO
        public.state_status
            (state_id)
        VALUES
            (%s);
"""

get_time_stamps_for_toggleable_state_change_today = """
select 
    s.*,
    (timestamp at time zone 'utc' at time zone 'america/denver') as time
from toggleable_status s
where 
	DATE_TRUNC('day', (timestamp at time zone 'utc' at time zone 'america/denver')) =
	DATE_TRUNC('day', (now() at time zone 'america/denver'))
	and 
	s.toggleable_id = %s

order by timestamp asc
"""

get_last_time_stamp_for_toggleabale_state_change = """
select 
    s.*,
    (timestamp at time zone 'utc' at time zone 'america/denver') as time
from toggleable_status s
where 
	DATE_TRUNC('day', (timestamp at time zone 'utc' at time zone 'america/denver')) =
	DATE_TRUNC('day', ((now() - interval '1' day) at time zone 'america/denver'))
	and 
	s.toggleable_id = %s

order by timestamp asc
limit 1"""
