from flask import Flask, render_template, request
import qrcode
import base64
import codecs
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(input_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_data = codecs.decode(base64.b64encode(img_buffer.getvalue()), 'ascii')

        # Save image to file
        with open('qr.png', 'wb') as f:
            f.write(img_buffer.getvalue())

        return render_template('gen.html', input_text=input_text, img_data=img_data)
    else:
        return render_template('gen.html')

if __name__ == '__main__':
    app.run(debug=True)
