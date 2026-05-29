import hashlib
import os
import time


def truncated_md5(data: bytes, bits: int) -> bytes:
    return hashlib.md5(data).digest()[: bits // 8]


def find_collision(bits: int = 24) -> tuple[bytes, bytes, int]:
    pairs = {}  # create a dict with pairs (hash and messages)
    attempts = 0  # counter of attempts
    while True:
        enter = os.urandom(8)  # randomly taken message
        hash_ = truncated_md5(enter, bits)  # hashing the message
        attempts += 1  # +1 attempt
        if (
            hash_ in pairs and pairs[hash_] != enter
        ):  # cheking if hash is already i n dict and if original messages are different
            return (
                pairs[hash_],
                enter,
                attempts,
            )  # returning first and second messages and amount of attempts until finding collision
        pairs[hash_] = enter  # adding new pair into dict


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
