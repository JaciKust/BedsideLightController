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
