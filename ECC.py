def extended_gcd(a, b):
    """
    Compute the extended Euclidean algorithm to find the greatest common divisor and the modular inverse.

    Parameters:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        tuple: A tuple (gcd, x, y), where gcd is the greatest common divisor, and x, y are the coefficients
               such that ax + by = gcd.
    """
    last_remainder, remainder = abs(a), abs(b)
    x, last_x, y, last_y = 0, 1, 1, 0

    while remainder:
        last_remainder, (quotient, remainder) = remainder, divmod(last_remainder, remainder)
        x, last_x = last_x - quotient * x, x
        y, last_y = last_y - quotient * y, y

    return last_remainder, last_x * (-1 if a < 0 else 1), last_y * (-1 if b < 0 else 1)


def modinv(a, m):
    """
    Compute the modular inverse of 'a' modulo 'm'.

    Parameters:
        a (int): The integer for which to find the modular inverse.
        m (int): The modulo value.

    Returns:
        int: The modular inverse of 'a' modulo 'm'.

    Raises:
        ValueError: If the modular inverse does not exist.
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist.")
    return x % m


def ecc_double(x, y, p, a):
    """
    Perform point doubling on the elliptic curve.

    Parameters:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
        p (int): The prime modulus.
        a (int): The coefficient 'a' in the elliptic curve equation.

    Returns:
        tuple: A tuple (x3, y3) representing the new point after doubling.
    """
    s = ((3 * (x ** 2) + a) * modinv(2 * y, p)) % p
    x3 = (s ** 2 - x - x) % p
    y3 = (s * (x - x3) - y) % p
    return x3, y3


def ecc_add(x1, y1, x2, y2, p, a):
    """
    Perform point addition on the elliptic curve.

    Parameters:
        x1 (int): The x-coordinate of the first point.
        y1 (int): The y-coordinate of the first point.
        x2 (int): The x-coordinate of the second point.
        y2 (int): The y-coordinate of the second point.
        p (int): The prime modulus.
        a (int): The coefficient 'a' in the elliptic curve equation.

    Returns:
        tuple: A tuple (x3, y3) representing the new point after addition.
    """
    if x1 == x2:
        s = ((3 * (x1 ** 2) + a) * modinv(2 * y1, p)) % p
    else:
        s = ((y2 - y1) * modinv(x2 - x1, p)) % p

    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return x3, y3


def double_and_add(scalar, generator, p, a):
    """
    Perform double-and-add algorithm to calculate the scalar multiplication of a point on the elliptic curve.

    Parameters:
        scalar (int): The scalar value.
        generator (tuple): A tuple (x, y) representing the generator point.
        p (int): The prime modulus.
        a (int): The coefficient 'a' in the elliptic curve equation.

    Returns:
        tuple: A tuple (x3, y3) representing the resulting point after scalar multiplication.
    """
    x3, y3 = 0, 0
    x1, y1 = generator
    x_tmp, y_tmp = generator
    init = 0

    for i in str(bin(scalar)[2:]):
        if i == '1' and init == 0:
            init = 1
        elif i == '1' and init == 1:
            x3, y3 = ecc_double(x_tmp, y_tmp, p, a)
            x3, y3 = ecc_add(x1, y1, x3, y3, p, a)
            x_tmp, y_tmp = x3, y3
        else:
            x3, y3 = ecc_double(x_tmp, y_tmp, p, a)
            x_tmp, y_tmp = x3, y3

    return x3, y3


def encrypt(plain_point, public_key, p, a):
    """
    Encrypt a point on the elliptic curve using elliptic curve point addition.

    Parameters:
        plain_point (tuple): A tuple (x, y) representing the point to be encrypted.
        public_key (tuple): A tuple (x, y) representing the public key for encryption.
        p (int): The prime modulus.
        a (int): The coefficient 'a' in the elliptic curve equation.

    Returns:
        tuple: A tuple (x, y) representing the encrypted point.
    """
    cipher_point = ecc_add(plain_point[0], plain_point[1], public_key[0], public_key[1], p, a)
    return cipher_point


def decrypt(cipher_point, private_key, p, a):
    """
    Decrypt a point on the elliptic curve using elliptic curve point addition.

    Parameters:
        cipher_point (tuple): A tuple (x, y) representing the point to be decrypted.
        private_key (tuple): A tuple (x, y) representing the private key for decryption.
        p (int): The prime modulus.
        a (int): The coefficient 'a' in the elliptic curve equation.

    Returns:
        tuple: A tuple (x, y) representing the decrypted point.
    """
    decrypted_point = ecc_add(cipher_point[0], cipher_point[1], private_key[0], -1 * private_key[1], p, a)
    return decrypted_point
