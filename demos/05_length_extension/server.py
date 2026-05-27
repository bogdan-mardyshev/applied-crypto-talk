"""
Demo 05 — Flask сервер с уязвимой MAC-схемой.

Схема: token = MD5(SECRET || payload)  ← уязвима к length extension!
"""

import hashlib
import hmac

from flask import Flask, jsonify, request

app = Flask(__name__)

# В реальном проекте: SECRET = os.environ["TOKEN_SECRET"]
SECRET = b"s3cr3t_k3y"  # 10 байт


# ---------------------------------------------------------------------------
# ТВОЯ ЗАДАЧА: реализовать две функции создания токена
# ---------------------------------------------------------------------------

def make_vulnerable_token(data: bytes) -> str:
    """Уязвимая схема: MD5(SECRET || data).

    Подсказка: hashlib.md5(SECRET + data).hexdigest()
    """
    raise NotImplementedError("Реализуй уязвимый токен")


def make_safe_token(data: bytes) -> str:
    """Безопасная схема: HMAC-MD5(key=SECRET, msg=data).

    Подсказка: hmac.new(SECRET, data, hashlib.md5).hexdigest()
    Почему не уязвима: HMAC = H((K⊕opad) || H((K⊕ipad) || m))
    """
    raise NotImplementedError("Реализуй HMAC токен")


# ---------------------------------------------------------------------------
# Endpoints (не менять логику роутов)
# ---------------------------------------------------------------------------

def verify_vulnerable_token(data: bytes, token: str) -> bool:
    return make_vulnerable_token(data) == token


def verify_safe_token(data: bytes, token: str) -> bool:
    return hmac.compare_digest(make_safe_token(data), token)


@app.route("/login", methods=["POST"])
def login():
    """POST /login {"username": "alice"}
    → {"token": "...", "payload": "...", "secret_len": 10}
    """
    body = request.get_json(force=True)
    username = "".join(c for c in body.get("username", "guest") if c.isalnum())
    payload = f"username={username}&role=user".encode()
    return jsonify({
        "token": make_vulnerable_token(payload),
        "payload": payload.decode(),
        "secret_len": len(SECRET),
    })


@app.route("/admin", methods=["GET"])
def admin():
    payload = request.args.get("payload", "").encode("latin-1")
    token   = request.args.get("token", "")
    if not verify_vulnerable_token(payload, token):
        return jsonify({"error": "invalid token"}), 403
    if b"role=admin" not in payload:
        return jsonify({"error": "not admin"}), 403
    return jsonify({"secret": "FLAG{length_extension_pwned_naive_mac}"})


@app.route("/admin-safe", methods=["GET"])
def admin_safe():
    payload = request.args.get("payload", "").encode("latin-1")
    token   = request.args.get("token", "")
    if not verify_safe_token(payload, token):
        return jsonify({"error": "invalid HMAC — length extension blocked"}), 403
    if b"role=admin" not in payload:
        return jsonify({"error": "not admin"}), 403
    return jsonify({"message": "HMAC safe — you got here legitimately"})


if __name__ == "__main__":
    print(f"[*] Сервер на http://0.0.0.0:5000  (SECRET len={len(SECRET)})")
    app.run(host="0.0.0.0", port=5000, debug=False)
