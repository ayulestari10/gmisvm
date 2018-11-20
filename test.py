import matplotlib.pyplot as plt 

plt.plot([0, 1, 2, 3, 4, 5, 6], [9.8, 18.25, 16.17, 14.53, 13.95, 10.48, 14.26], linestyle='-', marker='o', color='b')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['MC', 'DC', 'RS', 'GNB', 'NC', 'MLP', 'SGD'])

plt.xlabel('Metode Klasifikasi')
plt.ylabel('Rata-Rata Akurasi')
plt.title('Perbandingan Metode Klasifikasi dan Rata-Rata Akurasi')
plt.grid(True)
plt.show()