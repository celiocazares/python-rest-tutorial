import requests

BASE = "http://127.0.0.1:5000/"

data = [{
    "name": "video 1",
    "views": 10000,
    "likes": 100
}, {
    "name": "video 2",
    "views": 45566,
    "likes": 5000
}, {
    "name": "video 3",
    "views": 156456,
    "likes": 40664
}, {
    "name": "video 4",
    "views": 125645064065,
    "likes": 641065
}]

# INSERT INTO DATABASE
for index in range(len(data)):
    requests.put(BASE + "video/" + str(index + 1), data[index])

# print(response.json())

# response = requests.get(BASE + "video/1")
# print(response.json())

# UPDATE
# response = requests.patch(BASE + "video/1", {"name": "video update"})

# DELETE
# response = requests.delete(BASE + "video/4")
# print(response.json())
