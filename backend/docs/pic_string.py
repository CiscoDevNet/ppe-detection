import base64

with open("test.jpg", "rb") as imageFile:
    base64_bytes = base64.b64encode(imageFile.read())
    base64_string = base64_bytes.decode('utf-8')
    print(base64_string)

fh = open("converted.jpg", "wb")
fh.write(base64.b64decode(base64_string))
fh.close()
