import qrcode
import cv2

# qr = qrcode.make("hello world")
# qr.save('my_qr_code_png')

'''
https://pypi.org/project/qrcode/
@param
version (size_qr_code) int[1,40]
error_correction [7,15,30]%
box_size (size_img)
border (size_border)
'''

qr = qrcode.QRCode(
    version=1,
    box_size=15,
    border=5
)

# QR Code data
data = "POINT_3"

# append data
qr.add_data(data)
# auto fit QR config
qr.make(fit=True)

# set QR color and save
img = qr.make_image(fill='black', back_color='white')

img.save(f'resource/{data}.png')

# put Text on image
bk_img = cv2.imread(f'resource/{data}.png')
cv2.putText(bk_img, str(data), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imshow(str(data), bk_img)
cv2.waitKey()

#cv2.imwrite("resource/Add_Text.png", bk_img)
