import base64

data = "Y29mY3tqdTV0X3J1bl8xdH0="
message = base64.b64decode(data).decode()

print("Welcome to the club! Here's your first flag:")
print(message)
