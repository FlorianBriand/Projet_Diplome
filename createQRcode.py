import qrcode

img = qrcode.make('test')

img.save('qrcode.png')