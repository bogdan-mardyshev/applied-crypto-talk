"""
Demo 03 — Textbook RSA: Chosen-Ciphertext Attack.

Задача: реализовать RSA без паддинга и CCA через мультипликативное свойство.

Математика:
    RSA:          C = M^e mod n,   M = C^d mod n
    Свойство:     E(M1) * E(M2) = E(M1 * M2)  mod n

Атака (без знания d):
    1. Перехватить C = M^e mod n
    2. Выбрать r: gcd(r, n) = 1
    3. C' = C * r^e mod n  →  отправить в decryption oracle
    4. M' = oracle(C') = M * r mod n
    5. M  = M' * r^(-1) mod n

Запуск: python demo.py
"""

import math

# --- Маленькие простые числа для наглядности (не для реального RSA!) ---
_P = 61
_Q = 53
_N = _P * _Q  # 3233
_E = 17  # открытая экспонента
_PHI = (_P - 1) * (_Q - 1)  # 3120
_D = pow(_E, -1, _PHI)  # приватная экспонента = 2753


# ---------------------------------------------------------------------------
# ТВОЯ ЗАДАЧА
# ---------------------------------------------------------------------------


def rsa_encrypt(m: int, e: int, n: int) -> int:
    """Textbook RSA шифрование: C = M^e mod n.

    Подсказка: pow(m, e, n) — встроенная функция Python для быстрого возведения
    в степень по модулю. Проверь что m < n.
    """
    raise NotImplementedError("Реализуй RSA encrypt")


def rsa_decrypt(c: int, d: int, n: int) -> int:
    """Textbook RSA расшифрование: M = C^d mod n."""
    raise NotImplementedError("Реализуй RSA decrypt")


def decryption_oracle(c: int) -> int:
    """Симуляция decryption oracle.

    В реальной атаке это удалённый сервер. Oracle расшифровывает любой
    шифртекст кроме 'запрещённого' C — но он не может его отличить от C'!

    Просто вызови rsa_decrypt с правильными параметрами.
    """
    raise NotImplementedError("Реализуй oracle через rsa_decrypt")


def cca_attack(ciphertext: int, e: int, n: int, r: int) -> int:
    """CCA на textbook RSA через мультипликативное свойство.

    Шаги (расписаны в module docstring выше):
        1. blinded_ct = (ciphertext * pow(r, e, n)) % n
        2. blinded_pt = decryption_oracle(blinded_ct)  →  = M * r mod n
        3. r_inv      = pow(r, -1, n)                  ←  модульное обратное
        4. M          = (blinded_pt * r_inv) % n

    Условие: gcd(r, n) == 1  (иначе pow(r,-1,n) упадёт)
    """
    if math.gcd(r, n) != 1:
        raise ValueError("r должен быть взаимно прост с n")
    raise NotImplementedError("Реализуй CCA атаку")


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 58)
    print("  Textbook RSA — Chosen-Ciphertext Attack")
    print("=" * 58)

    n, e = _N, _E
    secret = 42  # секретное сообщение

    print(f"\n[*] Параметры: n={n}, e={e}, d={_D}")
    print(f"[*] Секрет M = {secret}")

    c = rsa_encrypt(secret, e, n)
    print(f"[*] Шифртекст C = {c}")

    r = 2
    recovered = cca_attack(c, e, n, r)
    print(f"\n[+] Восстановленный M = {recovered}")
    print(f"[+] Атака успешна: {recovered == secret}")


if __name__ == "__main__":
    main()
