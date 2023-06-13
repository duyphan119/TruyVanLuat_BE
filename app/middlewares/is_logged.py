def is_logged(session):
    if "user_id" in session:
        return True
    return False
