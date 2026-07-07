import getpass
from models.user_model import add_user

def create_admin():
    print("=== Create Initial Admin User ===")
    
    # 1. Gather input from the terminal
    full_name = input("Full Name: ")
    email = input("Email Address: ")
    username = input("Username: ")
    
    # getpass hides the password as you type it
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    
    if password != confirm_password:
        print("\nError: Passwords do not match. Aborting.")
        return
        
    contact_number = input("Contact Number (Optional): ")

    # 2. Pass the raw data to your UserModel 
    # (The model handles the password hashing and database insertion!)
    success = add_user(
        full_name=full_name,
        email=email,
        username=username,
        password=password,
        role="Owner/ Admin",
        contact_number=contact_number if contact_number else None
    )

    # 3. Output result
    if success:
        print(f"\nSuccess! Admin user '{username}' has been created.")
    else:
        print(f"\nFailed to create user. Please check your console for database errors.")

if __name__ == "__main__":
    create_admin()