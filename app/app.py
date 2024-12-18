from flask import Flask, request, jsonify
import os
import math
import json
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops, ImageOps
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CONFIG_FILE = "users_config.json"

def load_user_config(chat_id):
    try:
        with open(CONFIG_FILE, 'r') as file:
            configs = json.load(file)
            return configs.get(str(chat_id), 
            {
                "size": 40,
                "color": "#C6C6C6",
                "opacity": 0.25,
                "space_x": 160,
                "space_y": 110,
                "angle": 30
            })
    except:
        return {
                "size": 40,
                "color": "#C6C6C6",
                "opacity": 0.25,
                "space_x": 150,
                "space_y": 110,
                "angle": 30
                }

def save_user_config(chat_id, config):
    try:
        with open(CONFIG_FILE, 'r') as file:
            configs = json.load(file)
    except:
        configs = {}

    configs[str(chat_id)] = config
    with open(CONFIG_FILE, 'w') as file:
        json.dump(configs, file, indent=4)

# Add watermark to the image and send it
def add_mark(image_path, mark, chat_id):
    response = requests.get(image_path)

    im = Image.open(BytesIO(response.content))
    im = ImageOps.exif_transpose(im)
    image = mark(im)

    name = os.path.basename(image_path)
    if image:
        output = image_to_bytes(image)
        send_photo(chat_id, output, "")

# Set watermark opacity
def set_opacity(im, opacity):
    assert 0 <= opacity <= 1
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

# Crop empty edges of the image
def crop_image(im):
    bg = Image.new(mode='RGBA', size=im.size)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    del bg
    if bbox:
        return im.crop(bbox)
    return im

# Generate watermark image
def gen_mark(watermark_text, chat_id):
    config = load_user_config(chat_id)

    size = config["size"]
    color = config["color"]
    opacity = config["opacity"]
    space_x = config["space_x"]
    space_y = config["space_y"]
    angle = config["angle"]

    font_family = "./font.ttf"
    font_height_crop = 1.2
    mark = watermark_text

    width = len(mark) * size
    height = int(size * font_height_crop)
    mark_image = Image.new(mode='RGBA', size=(width, height))
    draw = ImageDraw.Draw(mark_image)
    draw.text(xy=(0, 0), text=mark, fill=color, font=ImageFont.truetype(font_family, size=size))
    del draw
    mark_image = crop_image(mark_image)
    set_opacity(mark_image, opacity)

    def mark_im(im):
        c = int(math.sqrt(im.size[0] * im.size[0] + im.size[1] * im.size[1]))
        mark2 = Image.new(mode='RGBA', size=(c, c))
        y, idx = 0, 0
        while y < c:
            x = -int((mark_image.size[0] + space_x) * 0.5 * idx)
            idx = (idx + 1) % 2
            while x < c:
                mark2.paste(mark_image, (x, y))
                x = x + mark_image.size[0] + space_x
            y = y + mark_image.size[1] + space_y
        mark2 = mark2.rotate(angle)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        im.paste(mark2, (int((im.size[0] - c) / 2), int((im.size[1] - c) / 2)), mask=mark2.split()[3])
        del mark2
        return im

    return mark_im

# Convert image to byte array
def image_to_bytes(image):
    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output.getvalue()

# Send photo
def send_photo(chat_id, photo_bytes, name):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    files = {'photo': photo_bytes}
    payload = {'chat_id': chat_id, 'caption': name, 'has_spoiler': True}
    response = requests.post(url, files=files, data=payload)
    return response.json()

def get_photo_url(photo_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile"
    params = {'file_id': photo_id}
    response = requests.get(url, params=params)
    data = response.json()
    file_path = data['result']['file_path']
    return f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

def delete_message(chat_id, message_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteMessage"
    payload = {
        'chat_id': chat_id,
        'message_id': message_id
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']

        if 'text' in message:
            text = message['text'].strip()
            if text.startswith("/set"):
                parts = text.split()
                if len(parts) < 3:
                    send_message(chat_id, (
                        "Usage: /set <key> <value>\n\n"
                        "Available keys:\n"
                        "- size [default:40]\n"
                        "- opacity [default:0.20]\n"
                        "- space_x [default:160]\n"
                        "- space_y [default:110]\n"
                        "- angle [default:30]"
                    ))
                    return jsonify({'status': 'ok'})

                key, value = parts[1], parts[2]
                current_config = load_user_config(chat_id)

                try:
                    if key in ["size", "space_x", "space_y", "angle"]:
                        value = int(value)
                    elif key == "opacity":
                        value = float(value)
                        
                    current_config[key] = value
                    save_user_config(chat_id, current_config)
                    send_message(chat_id, f"Configuration updated: {key} = {value}")
                except ValueError as e:
                    print(e)
                    send_message(chat_id, f"Invalid value for {key}. Please try again.")

                return jsonify({'status': 'ok'})

        if 'photo' in message:
            photo = message['photo'][-1]
            photo_id = photo['file_id']

            caption = message.get('caption', '').strip()
            if caption != "":
                watermark_text = caption
                photo_url = get_photo_url(photo_id)

                mark = gen_mark(watermark_text, chat_id)
                add_mark(photo_url, mark, chat_id)

                # Delete the original photo
                message_id = message['message_id']
                delete_message(chat_id, message_id)
            else:
                text = "Please send a photo with the caption to add a watermark."
                send_message(chat_id, text)
        else:
            text = "Please send a photo with a caption to add a watermark. \nUse /set to customize size, opacity, space, or angle."
            send_message(chat_id, text)

    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
