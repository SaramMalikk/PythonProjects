# print("Welcome to the Game. Guess the number")
# number = int(input("Enter the number "))
# attempts = 0
# while True:
#     guess_number = int(input('Guess the correct number '))
#     attempts += 1
#     if guess_number == number:
#         print('Congrats You guess the Correct number.')
#         break
#     else:
#         print("Wrong number")
#
#
# length = int(input('Enter the length '))
# lista = []
# for i in range(length):
#     number = int(input('Enter the number '))
#     lista.append(number)
# for i in lista:
#     if i % 2 == 0:
#         print(f"{i} ia a even number")
#     else:
#         print(f"{i} is a odd number")

# nums = range(1, 1000)
#
#
# def is_prime(num):
#     if num < 2:
#         return False
#
#     for i in range(2, int(num ** 0.5) + 1):
#         if num % i == 0:
#             return False
#     return True
#
#
# filter_by = list(filter(is_prime, nums))
# print("THESE are the list of Prime Numbers", filter_by)
#
# nums = [2,3,4,5,6,7,8]
# def is_even(num):
#     if num % 2 == 0:
#         return False
#     else:
#         return True
# hi = list(map(lambda x: x+3, nums))
# # print(hi)
# print(f"This is the list of odd numbers {is_even}")


import bcrypt
password = input("Enter Password ")
token = bcrypt.gensalt()
hash_password = bcrypt.hashpw(password.encode('utf-8'), token)
print(hash_password)
again = input("Enter the given Password ")
encode_pass = again.encode('utf-8')
print(encode_pass)
tries = 0
while True:
    if bcrypt.checkpw(encode_pass, hash_password):
        print('Hello welcome to the page')
        break
    elif tries == 4:
        print("Your attempts are finish try again later ")
        break
    else:
        again_ask = input("Wrong Password. Please Enter the Correct Password ")
        encode_pass = again_ask.encode('utf-8')
        tries += 1

