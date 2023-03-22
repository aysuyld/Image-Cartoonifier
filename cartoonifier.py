import cv2 #görüntü işleme için
import easygui #dosya kutusunu açmak için
import numpy as np #görüntüyü saklamak için
import imageio #beirli bir yolda saklanan görüntüyü okumak için
import sys
import matplotlib.pyplot as plt #görüntülerin grafiğini oluşturmak için
import os #yolu okumak ve görüntüleri o yola kaydetmek için
from tkinter import messagebox
#from tkinter import filedialog
from tkinter import *
#from PIL import ImageTk, Image

#-------Dosya kutusu oluşturma-------
def upload():
    global ImagePath
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    global ReSized6

    #resmi okuma
    originalmage =cv2.imread(ImagePath) #sayı biçiminde depolamak için
    originalmage =cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    #görüntü seçildi mi
    if originalmage is None:
        print("Hiçbir resim bulunamadı. Uygun dosyayı seçin")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (845,768)) #benzer bir ölçüde görüntülemek için yeniden boyutlandırma
    #plt.imshow(ReSized1, cmap='gray')

    #bir görüntüyü gri tonlamaya dönüştürme
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (845,768))
    #plt.imshow(ReSized2, cmap='gray')

    #gri tonlamalı bir görüntüyü yumuşatma
    blurGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(blurGrayScale, (845,768))
    #plt.imshow(ReSized3, cmap='gray')

    #çizgi film efekti için eşikleme tekniğini kullanarak kenarları alma
    getEdge = cv2.adaptiveThreshold(blurGrayScale, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (845,768))
    #plt.imshow(ReSized4, cmap='gray')

    #maske görüntüsü (telefonumuzdaki Beutify ya da AI efekti)
    #ikili filtre uygulama
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (845,768))
    #plt.imshow(ReSized5, cmap='gray')

    #çizgi film efekti vermek
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (845,768))
    #plt.imshow(ReSized6, cmap='gray')

    #tüm grafikleri çizmek
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes = plt.subplots(3, 2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    
    plt.show()

def save(Resized6, ImagePath):
    name = "cartoonified_image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, name+extension)
    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_RGB2BGR))
    text = "Image saved by name "+name+" at "+path
    messagebox.showinfo(title=None, message=text)

root = Tk()
root.geometry('400x400')
root.title('Cartoonifier')
root.configure(background='white')

label = Label(root, bg='blue', font=('calibri', 20, 'bold'))

upload_image = Button(root, text="Let's do it!", command=upload, padx=10, pady=5)
upload_image.configure(bg='indian red', fg='white', font=('calibri', 10, 'bold'))
upload_image.pack(side=TOP, pady=70)

save_image = Button(root, text="Save cartoon image", command=lambda: save(ReSized6, ImagePath), padx=30, pady=5)
save_image.configure(bg='indian red', fg='white', font=('calibri', 10, 'bold'))
save_image.pack(side=TOP, pady=50)

root.mainloop()

#upload()

