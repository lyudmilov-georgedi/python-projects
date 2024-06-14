import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

if __name__ == "__main__":
    num_passwords = int(input("Enter the number of passwords to generate: "))
    password_length = int(input("Enter the length of each password: "))

    for i in range(num_passwords):
        password = generate_password(password_length)
        print(f"Password {i+1}: {password}")
8