import pywhatkit
try:
    pywhatkit.sendwhatmsg_instantly(
        "+923114234004",
        "hello moon",
    )
    print("Message typed successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
# time.sleep(15)  # In Python, time.sleep() is a function from the time module that pauses the
# # execution of the program for a specified amount of time.


