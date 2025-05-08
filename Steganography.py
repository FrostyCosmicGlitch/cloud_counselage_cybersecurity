from tkinter import filedialog, Tk
from PIL import Image


SECRET_MESSAGE = "cloud counselage internship program"


def encode_message(image_path, message):
    img = Image.open(image_path)
    binary_message = ''.join([format(ord(i), '08b') for i in message]) + '1111111111111110'  

    if img.mode != 'RGB':
        img = img.convert('RGB')

    data = list(img.getdata())
    new_data = []

    msg_index = 0
    for pixel in data:
        if msg_index < len(binary_message):
            r = pixel[0] & ~1 | int(binary_message[msg_index])
            msg_index += 1
        else:
            r = pixel[0]

        if msg_index < len(binary_message):
            g = pixel[1] & ~1 | int(binary_message[msg_index])
            msg_index += 1
        else:
            g = pixel[1]

        if msg_index < len(binary_message):
            b = pixel[2] & ~1 | int(binary_message[msg_index])
            msg_index += 1
        else:
            b = pixel[2]

        new_data.append((r, g, b))

    img.putdata(new_data)
    img.save("output_encoded.png")
    print("Message encoded into image and saved as output_encoded.png")


def decode_message(image_path):
    img = Image.open(image_path)
    binary_data = ""
    for pixel in list(img.getdata()):
        for value in pixel[:3]:
            binary_data += str(value & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in all_bytes:
        if byte == "11111110":
            break
        message += chr(int(byte, 2))

    print("Decoded message:", message)
root = Tk()
root.withdraw()
image_path = filedialog.askopenfilename(title="Select Image to Encode/Decode")

if not image_path:
    print("No file selected.")
else:
    print("Selected:", image_path)
    encode_message(image_path, SECRET_MESSAGE)
    decode_message("output_encoded.png")
