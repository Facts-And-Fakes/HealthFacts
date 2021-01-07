dict = {"admin": {"id": 1, "password": "$5$rounds=535000$31BaUs31m/5qkfNA$UCHpgYUWfN.u6J4QG31jCXjjRW.a4wCMjhYAfCC2Sm3"}, "admin": {"id": 2, "password": "2CHpgYUWfN.u6J4QG31jCXjjRW.a4wCMjhYAfCC2Sm3"}}
username = "admin"
password = "admin"
filtered_dict = {k:v for (k,v) in dict.items() if username == k}
print(filtered_dict)