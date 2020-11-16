insert_state_update = """
    INSERT INTO
        public.toggleable_status
            (toggleable_id, state)
        VALUES
            (%s, %s);
"""
