"""
Demo 06 — MD5 Collision: Birthday Attack на усечённый хэш.

Вместо магических захардкоженных байт (Wang 2004) — объяснение КАК
работает birthday attack. Принцип тот же, что лежит в основе всех
collision attacks.

== Парадокс дней рождения ==

При n-битном хэше ожидаемое число попыток до коллизии ≈ 2^(n/2).

    MD5  (128 бит): теоретически 2^64 ≈ 1.8×10^19 попыток
    Wang 2004 (differential cryptanalysis): ~2^24 ≈ 16 млн
    Сегодня: fastcoll находит коллизию MD5 за <1 секунды

== Что делает эта демка ==

    16-бит prefix MD5 → коллизия за ~500 попыток  (мгновенно)
    24-бит prefix MD5 → коллизия за ~5000 попыток (мгновенно)

Ты увидишь в реальном времени как birthday attack находит коллизию.

ЗАДАЧА: реализовать find_collision() ниже.

Запуск: python demo.py
"""

import hashlib
import os
import time


def truncated_md5(data: bytes, bits: int) -> bytes:
    """Первые `bits` бит MD5 хэша (кратно 8).

    Пример: truncated_md5(b"hello", 16) → bytes длиной 2
    """
    return hashlib.md5(data).digest()[: bits // 8]


# ---------------------------------------------------------------------------
# ТВОЯ ЗАДАЧА
# ---------------------------------------------------------------------------


def find_collision(bits: int = 24) -> tuple[bytes, bytes, int]:
    seen = {}  # {хэш: сообщение}
    attempts = 0
    while True:
        msg = os.urandom(8)  # случайное 8-байтное сообщение
        h = truncated_md5(msg, bits)  # обрезанный хэш от входа
        attempts += 1
        if h in seen and seen[h] != msg:
            return seen[h], msg, attempts  # КОЛЛИЗИЯ! попалась сучка
        seen[h] = msg


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 58)
    print("  MD5 Birthday Attack Demo")
    print("=" * 58)
    print()
    print("Парадокс дней рождения:")
    print("  В группе 23 человек → >50% вероятность совпадения дней рождения")
    print("  Ищем ЛЮБУЮ пару, не конкретный день → 23*22/2=253 пары за 23 попытки")
    print()
    print("  Аналог с хэшами:")
    print("  Preimage:  'найти m с H(m)=0xdeadbeef' → 2^n попыток")
    print("  Collision: 'найти ЛЮБЫЕ m1≠m2 с H(m1)=H(m2)' → 2^(n/2) попыток")
    print()

    for bits in [16, 24]:
        print(f"[*] Ищем коллизию для {bits}-бит MD5...")
        start = time.time()

        msg1, msg2, attempts = find_collision(bits)

        elapsed = time.time() - start
        h1 = truncated_md5(msg1, bits)

        print(f"[+] Найдено за {attempts} попыток ({elapsed*1000:.1f} ms)")
        print(f"    msg1: {msg1.hex()}")
        print(f"    msg2: {msg2.hex()}")
        print(f"    H(msg1) = H(msg2) = {h1.hex()}  ✓")
        print(f"    msg1 != msg2: {msg1 != msg2}  ✓")
        print()

    print("[*] Для полного MD5 (128 бит):")
    print("    Birthday bound: ~2^64 ≈ 1.8×10^19 попыток — нереально без атаки")
    print("    Wang 2004 (differential cryptanalysis): ~2^24 — несколько минут (2004)")
    print("    fastcoll сегодня: < 1 секунды на обычном CPU")
    print()
    print("[!] Вывод: MD5 мёртв для security-задач. Используй SHA-256 или BLAKE3.")


if __name__ == "__main__":
    main()
