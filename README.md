# Elliptic Curve Cryptography (ECC) Image Encryption and Decryption

This project demonstrates image encryption and decryption using Elliptic Curve Cryptography (ECC). ECC is a public-key cryptographic system based on the mathematical properties of elliptic curves. In this project, we use ECC to encrypt an image, store the encrypted data, and then decrypt it back to its original form.

## Dependencies

To run this project, you will need the following dependencies:

- Python 3.x
- NumPy
- Matplotlib
- Pillow (PIL)

## Installation
1. Clone this repository to your local machine

```bash
git clone https://github.com/your-username/ecc-image-encryption.git
cd ecc-image-encryption
```

2. Install the required Python packages using pip:

```bash
pip install numpy matplotlib pillow
```

## Usage

0. ***Important: Before running the script, ensure that you update the file paths in the ecc_image_encryption.py file to point to the correct image file.***

1. Modify the ECC encryption and decryption keys, prime modulus, and coefficients in the ecc_image_encryption.py file according to your requirements. You can change the values of private_key_y, encryption_key_k, prime_modulus, coefficient_a, and coefficient_b.

2. Run the encryption and decryption process:

```bash
python ecc_image_encryption.py
```

3. The encrypted and decrypted images will be displayed using Matplotlib and saved to the project directory.

## How it Works

1. **Read Image**: The program reads an image file (in grayscale format) and converts it into a NumPy array, representing the pixel values.

2. **Generate Elliptic Curve Points**: The program generates all possible points on an elliptic curve defined by the equation y^2 ≡ x^3 + ax + b (mod p), where 'p' is a prime modulus, and 'a' and 'b' are coefficients defining the curve's shape. Only points satisfying the elliptic curve equation are considered.

3. **Map Pixels to Points**: Grayscale pixel values are mapped to the corresponding elliptic curve points. Each pixel value serves as an index to look up the list of possible points for that particular intensity value, creating a mapping between pixel intensities and elliptic curve points.

4. **Elliptic Curve Encryption and Decryption**:

- Generate Public and Private Keys: The program uses the double-and-add algorithm to perform scalar multiplication on a generator point 'g' (a base point on the curve). Scalar multiplication with a private key 'y' generates the public key 'pB' for encryption. Another scalar multiplication is performed with 'y' and 'k', chosen as the encryption key, to obtain 'kG', which will be used in the decryption process.
- Generate Encryption Key: The encryption key 'k' is chosen, and scalar multiplication with the public key 'pB' generates 'kPb', the encryption key used for encrypting the points.
- Encrypting Mapped Points: Each mapped point (pixel) is encrypted by adding it to 'kPb' using elliptic curve point addition. The encrypted points are stored in the 'encryptedPoints' list.
- Decrypting Mapped Points: Each encrypted point is decrypted by adding it to '-1 * ykG' using elliptic curve point addition, where 'ykG' is the result of scalar multiplication of 'y' (private key) with 'kG'. The decrypted points are stored in the 'decryptedPoints' list.

5. **Comparing Encrypted and Decrypted Points**: The program compares the original mapped points with the decrypted points. Any mismatches indicate an error in the encryption and decryption process.

6. **Image Reconstruction**: The program constructs the encrypted and decrypted images using the mapped pixel values and displays them using Matplotlib.

## Results

The encryptedImage and decryptedImage will be saved as image files and displayed using Matplotlib. Additionally, text files such as ImagePixelValue.txt, mappedPoints.txt, encryptedPoints.txt, and decryptedPoints.txt will be generated, containing relevant data for the image encryption and decryption process.

