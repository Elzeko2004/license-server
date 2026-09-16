from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# ============================================================
# قاعدة بيانات المفاتيح (مؤقتة - في الذاكرة)
# في المستقبل ممكن تستبدلها بقاعدة بيانات حقيقية (SQLite/PostgreSQL)
# ============================================================
VALID_KEYS = {
    # مثال: مفتاح -> بيانات
    "PRINCE-001": {"plan": "premium", "days": 30},
    "PRINCE-002": {"plan": "vip",     "days": 90},
    "TEST-KEY":   {"plan": "trial",   "days": 7},
}

# ============================================================
# المسار الأساسي اللي التطبيق بيتصل بيه
# ============================================================
@app.route('/api/mobile/license/verify', methods=['POST'])
def verify_license():
    try:
        data = request.json or request.form.to_dict() or {}
    except Exception:
        data = {}

    print(f"\n[+] New request received:")
    print(f"    Data: {data}")
    print(f"    Headers: {dict(request.headers)}")

    # استخراج البيانات (عدّل الأسماء حسب ما التطبيق يبعتها فعلاً)
    username     = data.get('username', '')
    password     = data.get('password', '')
    license_key  = data.get('license_key') or data.get('key') or username

    # التحقق من المفتاح
    if license_key in VALID_KEYS:
        info = VALID_KEYS[license_key]
        expires = (datetime.now() + timedelta(days=info['days'])).isoformat()

        print(f"[✅] Valid key: {license_key}")

        return jsonify({
            "success": True,
            "valid": True,
            "status": "active",
            "message": "License verified successfully",
            "username": username or license_key,
            "plan": info['plan'],
            "expires_at": expires,
            "days_remaining": info['days']
        }), 200
    else:
        print(f"[❌] Invalid key: {license_key}")
        return jsonify({
            "success": False,
            "valid": False,
            "status": "invalid",
            "message": "Invalid or expired license key"
        }), 401


# ============================================================
# مسار احتياطي للاختبار
# ============================================================
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "service": "License Server",
        "version": "1.0"
    })


@app.route('/reseller.json', methods=['GET'])
def reseller():
    return jsonify({"resellers": [], "status": "ok"})


# ============================================================
# تشغيل السيرفر
# ============================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)