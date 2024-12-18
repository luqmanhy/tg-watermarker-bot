<h1 align="center">Telegram Watermarker Bot</h1>

<p align="center">
Protect sensitive images with watermarks
</p>

<p align="center">
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-red.svg"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#credits">Credits</a> 
</p>

<p align="center">
<a href="https://github.com/luqmanhy/tg-watermarker-bot"><img src="/static/watermarker-demo.jpeg" alt="Watermarker Demo"></a>
</p>

---

## Overview
A Telegram bot that helps protect sensitive images by adding customizable watermarks. It ensures that your sensitive images remain confidential and secure from unauthorized use, making it an ideal tool for safeguarding your images.

## Key Features
- Customizable: Offers flexible customization options for text size, opacity, and designs to suit your preferences.
- Watermarking: Automatically adds a watermark to images based on the user's configuration.
- Delete Original Photos: Automatically delete the original images after watermarking.

## Deployment
### Telegram Setup (required)
1. Open Telegram and search for <a href="https://telegram.me/BotFather" target="_blank">@BotFather</a>.
2. Start a chat and send /newbot.
3. Choose a name and username for your bot.
4. Receive and save the Bot Token provided by BotFather.


### Deployment on Render
<a href="https://render.com" target="_blank">Render</a> provides a cloud hosting solution that simplifies application deployment without the need for server management. Follow these steps to deploy the bot on Render:
1. Go to <a href="https://render.com" target="_blank">Render</a> and log in to your account.
2. Click <b>"+ New"</b>  > <b>Web Service</b>
3. Choose <b>Source Code</b> > <b>Existing Image</b>
  - <b>Image URL</b> : luqmanhy/tg-watermarker-bot
4. Click <b>Connect</b>
5. Configure the service:
  - Add an environment variable:
    - <b>Key:</b> TELEGRAM_API_KEY
    - <b>Value:</b> Your Telegram Bot Token from BotFather.
6. Click <b>Deploy Web Service</b> to deploy

### Manual Deployment
If you prefer to deploy the bot on your own server, you can do so using the following methods:

### Using Docker
1. Clone the repository:
```bash
git clone https://github.com/luqmanhy/tg-watermarker-bot.git  
cd tg-watermarker-bot 
``` 
2. Set up the .env file with your Telegram Bot Token:
```bash
cp .env.example .env 
```
3. Build and run the Docker container:
```bash
docker build -t tg-watermarker-bot .  
docker run --name watermarker --env-file=.env -it tg-watermarker-bot 
```

### Manual Deployment (Without Docker)
1. Clone the repository:
```bash
git clone https://github.com/luqmanhy/tg-watermarker-bot.git  
cd tg-watermarker-bot  
```
2. Set up the .env file with your Telegram Bot Token :
```bash
cp .env.example .env  
```
3. Install the required Python packages:
```bash
pip install -r requirements.txt 
``` 
4. Run the application:
```bash
python3 app/app.py  
```

## Setting up the Webhook
Once the bot is running, you need to set up a webhook so Telegram can communicate with your bot:

1. Determine the URL of your hosted bot.
For Render, it will be something like https://your-app-name.onrender.com.
2. Use the following command to set up the webhook:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_API_TOKEN>/setWebhook" -d "url=<YOUR_BOT_URL>"  
``` 
Replace <b><YOUR_BOT_API_TOKEN></b> with your bot token and <b><YOUR_BOT_URL></b> with your deployed bot URL.

3. Verify the webhook setup:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_API_TOKEN>/getWebhookInfo"  
```
Ensure the response includes your bot URL and indicates that the webhook is set.
4. Test the bot by sending a message or image to ensure it works as expected.



## Usage
- Watermarking: When a photo is received with a caption, the bot adds the watermark based on the user's settings.
- Customize : /set commands allow users to update settings like size, opacity, space, and angle for watermarks.

## Customize options
Users can customize the following settings:

- size: Font size for watermark text.
- color: Color of the watermark text.
- opacity: Opacity of the watermark.
- space_x and space_y: Horizontal and vertical 
- spacing between watermarks.
- angle: Rotation angle of the watermark.

### Examples
```
/set size 50 - Set the watermark font size to 50.
/set opacity 0.5 - Set the opacity of the watermark to 0.5.
```

## Credits
### Contributing

We welcome contributions! Feel free to submit [Pull Requests](https://github.com/luqmanhy/tgwatermarker/pulls) or report [Issues](https://github.com/luqmanhy/tgwatermarker/issues).

### Licensing

This utility is licensed under the [MIT license](https://opensource.org/license/mit). You are free to use, modify, and distribute it, as long as you follow the terms of the license. You can find the full license text in the repository - [Full MIT license text](https://github.com/luqmanhy/tgwatermarker/blob/master/LICENSE).

