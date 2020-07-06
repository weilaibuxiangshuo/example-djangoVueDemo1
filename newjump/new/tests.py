
import requests
headers = {
    "Content-Type":"application/x-www-form-urlencoded"
}
for i in range(1):
    a = requests.post("http://127.0.0.1:8000",headers=headers,data={
        "username":i,
        "password":"admin888",
    })
    print(a.status_code)


# bb = "asdfjkl"
# print(bb[-2:])
# print(bb[-2:0])
# print(bb[0:-2])
# print(bb[:-2])
# print(bb[:2])
# print(bb[2:])