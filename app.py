from flask import Flask, render_template, request, session
import random
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# List of possible CAPTCHA characters
captcha_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def generate_captcha():
    captcha_text = ''.join(random.choices(captcha_chars, k=6))
    image = Image.new('RGB', (150, 50), color = (255, 255, 255))
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    draw.text((20, 15), captcha_text, fill=(0, 0, 0), font=font)
    image.save('captcha.png')
    return captcha_text

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_captcha = request.form['captcha']
        if 'captcha' in session and user_captcha == session['captcha']:
            if username == 'your_username' and password == 'your_password':
                return "Login successful!"
            else:
                return "Incorrect username or password."
        else:
            return "Incorrect CAPTCHA."

    session['captcha'] = generate_captcha()
    return render_template('login.html', captcha=session['captcha'])

if __name__ == '__main__':
    app.run(debug=True)
