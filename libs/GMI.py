from flask import Flask, Blueprint, abort
import numpy as np

class GMI():
    
    page = Blueprint('GMI_page', __name__, template_folder = 'templates')
    base = '/gmi'
    
    
    def __init__(self, img):
        self.matrix = img
        self.mt20 = 0
        self.mt02 = 0
        self.mt11 = 0
        self.mt30 = 0
        self.mt12 = 0
        self.mt21 = 0
        self.mt03 = 0
        self.ꞡ = self.x_bar()
        self.Ꞛ = self.y_bar()
    
    def hitungMomen(self, p, q):
        
        hasil = 0
        ukuran = self.matrix.shape
        for x in range(ukuran[0]):
            for y in range(ukuran[1]):
                hasil += (x**p) * (y**q) * (self.matrix[x][y])
        return hasil
        
    def hitungMomenPusat(self, p, q):
        hasil = 0
        ukuran = self.matrix.shape
        for x in range(ukuran[0]):
            for y in range(ukuran[1]):
                hasil += ((x - self.ꞡ)**p) * ((y - self.Ꞛ)**q) * (self.matrix[x][y])
        return hasil
        
    def x_bar(self):
        return self.hitungMomen(1, 0) / self.hitungMomen(0, 0)
        
    def y_bar(self):
        return self.hitungMomen(0, 1) / self.hitungMomen(0, 0)
        
    def momenNormalisasi(self, p, q):
        hasil = self.hitungMomenPusat(p, q)/ (self.hitungMomenPusat(0, 0) ** self.gamma(p, q))
        return hasil
    
    def gamma(self, p, q):
        return ((p+q)/2) + 1
        
    def hitungMomenNormalisasi(self):
        self.mt20 = self.momenNormalisasi(2, 0)
        self.mt02 = self.momenNormalisasi(0, 2)
        self.mt11 = self.momenNormalisasi(1, 1)
        self.mt30 = self.momenNormalisasi(3, 0)
        self.mt12 = self.momenNormalisasi(1, 2)
        self.mt21 = self.momenNormalisasi(2, 1)
        self.mt03 = self.momenNormalisasi(0, 3)
        print(f"mt20 = {self.mt20}")
        print(f"mt02 = {self.mt02}")
        print(f"mt11 = {self.mt11}")
        print(f"mt30 = {self.mt30}")
        print(f"mt12 = {self.mt12}")
        print(f"mt21 = {self.mt21}")
        print(f"mt03 = {self.mt03}")
        

    def hitungCiri(self):
        ciri = np.zeros((7))
        
        ciri[0] = self.mt20 + self.mt02
        ciri[1] = ((self.mt20 - self.mt02) ** 2) + 4 * (self.mt11 ** 2)
        ciri[2] = ( (self.mt30 - (3*self.mt12)) ** 2 ) + ( ((3*self.mt21) - self.mt03) ** 2)
        ciri[3] = ( (self.mt30 + self.mt12) ** 2 ) + ( (self.mt21 + self.mt03) ** 2 )
        ciri[4] = (self.mt30 - (3*self.mt12)) * (self.mt30 + self.mt12) * (((self.mt30 + self.mt12) ** 2) - (3 * ((self.mt21 + self.mt03) ** 2)) ) + ((3*self.mt21) - self.mt03) * (self.mt21 + self.mt03) * ( ( 3*(self.mt30 + self.mt12)**2 ) - ((self.mt21 + self.mt03) **2 ) )     
        ciri[5] = (self.mt20 - self.mt02) * ( ((self.mt30 + self.mt12) ** 2) - ((self.mt21 + self.mt03) ** 2) ) + 4 * self.mt11 * (self.mt30 + self.mt12) * (self.mt21 + self.mt03)
        ciri[6] = ((3*(self.mt21)) - self.mt03) * (self.mt30 + self.mt12) * ( ( (self.mt30 + self.mt12) ** 2) - (3 * (self.mt21 + self.mt03) ** 2) ) + ( (3*self.mt21) - self.mt30) * (self.mt21 + self.mt03) * ( (3*(self.mt30 + self.mt12) ** 2) - ((self.mt21 + self.mt03) ** 2) )
        
        return ciri