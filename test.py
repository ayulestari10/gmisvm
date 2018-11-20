import matplotlib.pyplot as plt 

plt.plot([0, 1, 2, 3, 4, 5, 6], [10.2, 14.73, 14.78, 14.73, 14.66, 11.09, 14.19], linestyle='-', marker='o', color='b')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['MC', 'DC', 'RS', 'GNB', 'NC', 'MLP', 'SGD'])

plt.xlabel('Metode Klasifikasi')
plt.ylabel('Rata-Rata Akurasi')
plt.title('Perbandingan Metode Klasifikasi dan Rata-Rata Akurasi')
plt.grid(True)
plt.show()