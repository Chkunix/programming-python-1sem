import qrcode

NAME = "Yaroslav"
SURNAME = "Korolchuk"
GROUP = "IT-31"

print(f"{NAME} {SURNAME}, {GROUP}")

text = "Korolchuk Yaroslav, IT-31, examplemail@gmail.com"
image = qrcode.make(text)
image.save("contact.png")
print("saved: contact.png")
