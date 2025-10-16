# backend/app.py
from flask import Flask, request, send_file
from flask_cors import CORS
import qrcode
import io

app = Flask(__name__)
CORS(app)  # อนุญาตให้เว็บอื่นเรียก API ได้

@app.route('/generate', methods=['POST'])
def generate_qr():
    try:
        data = request.json.get('text', '').strip()
        if not data:
            return {"error": "กรุณากรอกข้อความหรือลิงก์!"}, 400

        # สร้าง QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # ส่งรูปเป็น response
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return {"error": "เกิดข้อผิดพลาด: " + str(e)}, 500

# สำหรับ Render.com
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)