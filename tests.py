dict = {"admin": {"id": 1, "password": "$5$rounds=535000$31BaUs31m5qkfNA$UCHpgYUWfN.u6J4QG31jCXjjRW.a4wCMjhYAfCC2Sm3"}, "admin": {"id": 2, "password": "2CHpgYUWfN.u6J4QG31jCXjjRW.a4wCMjhYAfCC2Sm3"}}
from passlib.hash import sha256_crypt

print(sha256_crypt.verify("ollol","$5$rounds=535000$Y0g28yqb3ldGyPvt$REOUv7fX18K/obbBfQd3sIPVQKIpvjG1jEdDT8/HxlA"))