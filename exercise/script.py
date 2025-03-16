import random

# Simple class to represent a User
class User:
    def __init__(self, username, password, active=True):
        self.username = username
        self.password = password
        self.active = active

# User authentication system
def authenticate_user(username, password, user_list):
    for user in user_list:
        if user.username == username:
            if user.password == password and user.active:
                return True
            else:
                return False
    return False

# Check user privileges
def check_privileges(user, required_role, user_roles):
    return user_roles.get(user.username) == required_role

# Function for admin users
def admin_action(user):
    print(f"{user.username} has admin privileges: Access granted to confidential data.")

# Function for non-admin users
def user_action(user):
    print(f"{user.username} does not have admin privileges: Access granted to general data only.")

# Main execution
def main():
    users = [
        User("alice", "password123"),
        User("bob", "bobsecure"),
        User("charlie", "charliepass", active=False)
    ]

    user_roles = {
        "alice": "admin",
        "bob": "user",
        "charlie": "guest"
    }

    test_cases = [
        ("alice", "password123"),
        ("bob", "wrongpassword"),
        ("charlie", "charliepass"),
        ("dave", "nopassword")
    ]

    for username, password in test_cases:
        auth_result = authenticate_user(username, password, users)
        if auth_result:
            user = next(user for user in users if user.username == username)

            if check_privileges(user, "admin", user_roles):
                admin_action(user)
            else:
                user_action(user)

if __name__ == "__main__":
    main()
