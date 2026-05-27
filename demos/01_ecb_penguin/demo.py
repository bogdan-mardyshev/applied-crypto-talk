"""
Demo 01 — ECB Penguin: визуализация режимов блочного шифрования.

Задача: зашифровать изображение тремя режимами AES и сохранить результаты.
Ожидаемый эффект:
  - tux_ecb.png  → структура изображения ВИДНА (паттерны сохраняются)
  - tux_cbc.png  → случайный шум (паттерны убраны)
  - tux_gcm.png  → случайный шум (аутентифицированное шифрование)

Запуск: python demo.py
"""

import hashlib
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PIL import Image

# --- Детерминированные параметры (не менять — нужны для smoke-теста) ---
_SEED = b"applied-crypto-talk-2024-ecb-demo"
KEY: bytes = hashlib.sha256(_SEED).digest()   # 32 байта → AES-256
IV: bytes  = hashlib.md5(_SEED).digest()       # 16 байт  → CBC IV
NONCE: bytes = hashlib.md5(b"gcm-nonce").digest()[:12]  # 12 байт → GCM nonce

ASSETS_DIR = Path(__file__).parent / "assets"


# ---------------------------------------------------------------------------
# Вспомогательные функции (уже реализованы — используй в своих функциях)
# ---------------------------------------------------------------------------

def image_to_raw_bytes(path: Path) -> tuple[bytes, tuple[int, int]]:
    """Открыть PNG, вернуть сырые RGB-байты и размер (width, height)."""
    img = Image.open(path).convert("RGB")
    return img.tobytes(), img.size


def raw_bytes_to_image(data: bytes, size: tuple[int, int], path: Path) -> None:
    """Восстановить изображение из сырых RGB-байт и сохранить."""
    img = Image.frombytes("RGB", size, data)
    img.save(path)


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """PKCS#7 паддинг до кратного block_size байт."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


# ---------------------------------------------------------------------------
# ТВОЯ ЗАДАЧА: реализовать три функции шифрования
# ---------------------------------------------------------------------------

def encrypt_ecb(data: bytes, key: bytes) -> bytes:
    """AES-ECB: каждый 16-байтовый блок шифруется НЕЗАВИСИМО одним ключом.

    Формула: C_i = AES_K(P_i)

    Почему опасно: одинаковые блоки открытого текста → одинаковые блоки
    шифртекста. На изображении паттерны сохраняются.

    Подсказки:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        Cipher(algorithms.AES(key), modes.ECB())
        Не забудь pkcs7_pad перед шифрованием.
    """
    raise NotImplementedError("Реализуй AES-ECB шифрование")


def encrypt_cbc(data: bytes, key: bytes, iv: bytes) -> bytes:
    """AES-CBC: каждый блок XOR-ится с предыдущим шифртекстом.

    Формула: C_i = AES_K(P_i ⊕ C_{i-1}),  C_0 = IV

    Почему лучше ECB: даже одинаковые блоки дают разный шифртекст.
    Почему не достаточно: нет аутентификации (уязвим к padding oracle).

    Подсказки:
        modes.CBC(iv)
        Не забудь pkcs7_pad.
    """
    raise NotImplementedError("Реализуй AES-CBC шифрование")


def encrypt_gcm(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """AES-GCM: AEAD-режим (шифрование + аутентификация в одном).

    GCM = CTR-mode (stream cipher) + Poly1305 MAC.
    Возвращает только шифртекст без 16-байтового тега (для визуализации).

    Формула: C_i = P_i ⊕ AES_K(nonce ‖ counter_i)

    Подсказки:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        AESGCM(key).encrypt(nonce, data, associated_data=None)
        Результат = шифртекст (len(data) байт) + тег (16 байт) — обрежь тег.
    """
    raise NotImplementedError("Реализуй AES-GCM шифрование")


# ---------------------------------------------------------------------------
# main() — не менять структуру, только реализуй функции выше
# ---------------------------------------------------------------------------

def _create_synthetic_image() -> None:
    """Создать тестовое изображение с повторяющимися паттернами."""
    width, height = 128, 128
    pixels = []
    for y in range(height):
        color = (0, 0, 80 + (y // 16) * 20) if (y // 16) % 2 == 0 else (200, 200, 200)
        pixels.extend([color] * width)
    img = Image.new("RGB", (width, height))
    img.putdata(pixels)
    img.save(ASSETS_DIR / "tux.png")
    print("[*] Создано синтетическое изображение assets/tux.png")


def main() -> None:
    tux_path = ASSETS_DIR / "tux.png"
    if not tux_path.exists():
        print(f"[!] Нет файла {tux_path} — создаём синтетическое")
        _create_synthetic_image()

    raw_bytes, size = image_to_raw_bytes(tux_path)
    raw_len = len(raw_bytes)
    print(f"[*] Изображение: {size[0]}x{size[1]} px, {raw_len} байт")

    ecb_bytes = encrypt_ecb(raw_bytes, KEY)
    cbc_bytes = encrypt_cbc(raw_bytes, KEY, IV)
    gcm_bytes = encrypt_gcm(raw_bytes, KEY, NONCE)

    raw_bytes_to_image(ecb_bytes[:raw_len], size, ASSETS_DIR / "tux_ecb.png")
    raw_bytes_to_image(cbc_bytes[:raw_len], size, ASSETS_DIR / "tux_cbc.png")
    raw_bytes_to_image(gcm_bytes[:raw_len], size, ASSETS_DIR / "tux_gcm.png")

    print("[+] Сохранено: tux_ecb.png, tux_cbc.png, tux_gcm.png")
    print("    Открой их и сравни визуально — ECB должен быть 'читаемым'")


if __name__ == "__main__":
    main()
