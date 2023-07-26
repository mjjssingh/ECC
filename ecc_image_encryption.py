import itertools
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import ECC

prime_modulus = 751
coefficient_a = -1
coefficient_b = 188
generator_point = (0, 376)
private_key_y = 85

# Calculate public key pB
public_key_pB = ECC.double_and_add(private_key_y, generator_point, prime_modulus, coefficient_a)

# Calculate kPb for encryption
encryption_key_k = 113
encryption_key_kPb = ECC.double_and_add(encryption_key_k, public_key_pB, prime_modulus, coefficient_a)

# Calculate ykG for decryption
kG = ECC.double_and_add(encryption_key_k, generator_point, prime_modulus, coefficient_a)
decryption_key_ykG = ECC.double_and_add(private_key_y, kG, prime_modulus, coefficient_a)

xLabel = dict()
yLabel = dict()


def labelX(x):
    xLabel.setdefault((x ** 3 + (coefficient_a * x) + coefficient_b) % prime_modulus, []).append(x)


def labelY(y):
    yLabel.setdefault((y ** 2) % prime_modulus, []).append(y)


for num in range(0, prime_modulus):
    labelX(num)
    labelY(num)

intersect = []
for item in xLabel.keys():
    if yLabel.__contains__(item):
        tmp = list(itertools.product(xLabel[item], yLabel[item]))
        intersect = intersect + tmp

intersect.sort(key=lambda y: y[0])
print(len(intersect))
print("*******************")
print("Generated all Points of the elliptic curve successfully")

mappingList = [[] for _ in range(256)]
i = 0
t = 0
col = 1

while i < len(intersect):
    mappingList[t].append(intersect[i])
    t += 1
    if t == 256:
        t = 0
        col += 1
    i += 1

while t < 256:
    mappingList[t].append((0, 0))
    t += 1

print("*******************")
print('Created mapping list successfully')

with open('points.txt', 'w') as file:
    for points in mappingList:
        file.write(str(points) + "\n")

# Getting GrayScale values for image
file_path = '/Users/Jabez/PycharmProjects/ECC/lena.png'
image = Image.open(file_path).convert("L")
pixel_array = np.asarray(image)
plt.imshow(pixel_array, cmap='gray', vmin=0, vmax=255)
plt.show()
print(pixel_array.shape)

print("*******************")
print("Converted image to raw data Successfully!!")

# Storing raw data of the image to a file
with open('ImagePixelValue.txt', 'w') as file:
    for points in pixel_array:
        file.write(str(points) + "\n")

track = [0 for _ in range(256)]
mappedPoints = []

for i in range(50):
    l = []
    for j in range(50):
        c = mappingList[pixel_array[i][j]][track[pixel_array[i][j]]]
        track[pixel_array[i][j]] += 1
        if track[pixel_array[i][j]] >= 3:
            track[pixel_array[i][j]] = 0
        l.append(c)
    mappedPoints.append(l)

print("*******************")
print("Mapped pixels to Points Successfully!!")

with open('mappedPoints.txt', 'w') as file:
    for points in mappedPoints:
        file.write(str(points) + "\n")

encryptedPoints = []
for i in range(50):
    l = []
    for j in range(50):
        pM = mappedPoints[i][j]
        pC = ECC.encrypt(pM, encryption_key_kPb, prime_modulus, coefficient_a)
        l.append(pC)

    encryptedPoints.append(l)

print("*******************")
print("Encrypted Successfully!!")

with open('encryptedPoints.txt', 'w') as file:
    for points in encryptedPoints:
        file.write(str(points) + "\n")

decryptedPoints = []
for i in range(50):
    l = []
    for j in range(50):
        point = ECC.decrypt(encryptedPoints[i][j], decryption_key_ykG, prime_modulus, coefficient_a)
        l.append(point)
    decryptedPoints.append(l)

print("*******************")
print("Decrypted Successfully!!")

with open('decryptedPoints.txt', 'w') as file:
    for points in decryptedPoints:
        file.write(str(points) + "\n")

count = 0

for i in range(50):
    for j in range(50):
        if mappedPoints[i][j] != decryptedPoints[i][j]:
            count += 1

print("Number of mismatched points: ", count)


def findIntensity(mapped):
    for i in range(256):
        for j in range(3):
            if mapped == mappingList[i][j]:
                return i
    return 46


encryptedImage = []
for i in range(50):
    l = []
    for j in range(50):
        temp = findIntensity(encryptedPoints[i][j])
        l.append(temp)
    encryptedImage.append(l)

print("Encrypted Image constructed successfully!!")
plt.imshow(encryptedImage, cmap='gray', vmin=0, vmax=255)
plt.show()

decryptedImage = []
for i in range(50):
    l = []
    for j in range(50):
        temp = findIntensity(decryptedPoints[i][j])
        l.append(temp)
    decryptedImage.append(l)

print("Decrypted Image constructed successfully!!")

count = 0
for i in range(50):
    for j in range(50):
        if decryptedImage[i][j] != pixel_array[i][j]:
            count += 1

print("Pixels not found: ", count)
plt.imshow(decryptedImage, cmap='gray', vmin=0, vmax=255)
plt.show()
