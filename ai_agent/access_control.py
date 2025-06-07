AUTHORIZED_USERS = ["test_user_1", "admin"]

def check_permission(user_id, resource_type):
    if user_id not in AUTHORIZED_USERS:
        raise PermissionError(f"Access denied for user {user_id} to {resource_type} data.")
        return True