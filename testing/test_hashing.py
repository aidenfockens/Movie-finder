from werkzeug.security import generate_password_hash, check_password_hash

password = "test_password"
hashed_password = generate_password_hash(password)
print(f"Hashed Password: {hashed_password}")

# Check password
is_match = check_password_hash(hashed_password, password)
print(f"Password Match: {is_match}")