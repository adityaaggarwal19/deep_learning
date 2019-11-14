dict1 = {"www.abc.com": 4.1, "www.xyz.com": 5.2, "www.pqr.com": 4.5}
print(sorted(dict1.items(), key = lambda kv: kv[1], reverse = True)[:5])
