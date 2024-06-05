import datetime
from prettytable import PrettyTable
import os
import pwinput

class User:
    def __init__(self, username, password, age, gender, pin):
        self.username = username
        self.password = password
        self.age = age
        self.gender = gender
        self.pin = pin

class Admin(User):
    def __init__(self, username, password, age, gender, pin):
        super().__init__(username, password, age, gender, pin)

    def add_product(self, products):
        idx = len(products) + 1
        name = input("Nama Makanan/Minuman: ")
        stock = int(input("Jumlah Makanan/Minuman: "))
        price = int(input("Harga Makanan/Minuman: "))
        category = input("Kategori Makanan/Minuman: ")
        products.append(Product(idx, name, stock, price, category))
        print("Produk berhasil ditambahkan.")

    def remove_product(self, products):
        for i, product in enumerate(products):
            print(f"{i+1}. {product.name}")
        choice = int(input("Pilih nomor Makanan/Minuman yang ingin dihapus: ")) - 1
        if 0 <= choice < len(products):
            del products[choice]
            print("Makanan/Minuman berhasil dihapus.")
        else:
            print("Nomor Makanan/Minuman tidak valid.")

    def view_products(self, products):
        table = PrettyTable()
        table.field_names = ["Nama Makanan/Minuman", "Stok", "Harga", "Kategori"]
        for product in products:
            table.add_row([product.name, product.stock, product.price, product.category])
        print(table)

class Buyer(User):
    def __init__(self, username, password, age, gender, pin, e_money):
        super().__init__(username, password, age, gender, pin)
        self.e_money = e_money
        self.cart = []

    def greet_user(self):
        if 7 <= self.age <= 14:
            salutation = "Dek"
        elif 15 <= self.age <= 29:
            salutation = "Mba" if self.gender.lower() == 'famale' else "Mas"
        elif 30 <= self.age <= 75:
            salutation = "Pak" if self.gender.lower() == 'male' else "Bu"
        else:
            salutation = "Kakek/Nenek"
        print(f"\nSelamat datang, {salutation} {self.username}")

    def buy_product(self, products):
        cart = []
        while True:
            print("\nDaftar Menu:")
            table = PrettyTable()
            table.field_names = ["No", "Nama Makanan/Minuman", "Stok", "Harga", "Kategori"]
            for product in products:
                table.add_row([product.idx, product.name, product.stock, product.price, product.category])
            print(table)
            print("\nNB: TIAP PEMBELIAN DI ATAS 100K AKAN MENDAPAT DISKON 15% DAN DI ATAS 350K MENDAPAT DISKON 25%")

            while True:
                try:
                    choice = input("Pilih nomor produk yang ingin dimasukkan ke keranjang ('s' untuk selesai memilih): ")
                    if choice.lower() == 's':
                        break
                    choice = int(choice) - 1
                    if 0 <= choice < len(products):
                        break
                    else:
                        print("Nomor produk tidak valid.")
                except ValueError:
                    print("Input tidak valid. Masukkan angka yang sesuai.")

            if str(choice).lower() == 's':
                break

            while True:
                try:
                    quantity = int(input("Masukkan jumlah Makanan/Minuman yang ingin dibeli: "))
                    if quantity <= products[choice].stock:
                        break
                    else:
                        print("Stok Makanan/Minuman tidak mencukupi.")
                except ValueError:
                    print("Input tidak valid. Masukkan angka yang sesuai.")

            cart.append((products[choice], quantity))

        if not cart:
            print("Anda belum memilih Makanan/Minuman.")
            return

        total_price = sum(item[0].price * item[1] for item in cart)

        # Menerapkan potongan harga
        if total_price > 350000:
            discounted_price = total_price * 0.75
            total_discount = total_price - discounted_price
        elif total_price > 100000:
            discounted_price = total_price * 0.85
            total_discount = total_price - discounted_price
        else:
            discounted_price = total_price
            total_discount = 0

        # Pembayaran dengan e-money
        if self.e_money >= discounted_price:
            self.e_money -= discounted_price
            for item in cart:
                product, quantity = item
                product.stock -= quantity

            # Menampilkan nota pembelian
            clear()
            print("="*69)
            print("\nNota Pembelian:")
            print("TEA TIME")
            print("Jl. Kucing V No. 8, Samarinda")
            print("Tanggal Pembelian:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("Nama Pembeli:", self.username)
            nota = PrettyTable()
            nota.field_names = ["Nama Produk", "Jumlah", "Harga Satuan", "Total Harga"]
            for item in cart:
                product, quantity = item
                nota.add_row([product.name, quantity, product.price, product.price * quantity])
            print(nota)
            print("\nPembayaran menggunakan e-money.")
            print(f"Pembayaran berhasil.")
            print(f"Sisa e-money: {self.e_money}")
            if total_discount > 0:
                print(f"Total diskon: {total_discount}")
                print(f"Total harga yang anda bayarkan: {discounted_price}")
                print(f"Thank you for buying food and drinks from us, we hope you like it")
                print("="*69)
            else:
                print(f"Total harga yang anda bayarkan: {discounted_price}")
                print(f"Thank you for buying food and drinks from us, we hope you like it")
                print("="*69)
        else:
            print("\nSaldo e-money tidak mencukupi.")

    def top_up_emoney(self):
        print(f"E-money anda sekarang : {self.e_money}")
        amount = float(input("Masukkan jumlah uang yang ingin ditambahkan: "))
        self.e_money += amount
        print(f"Saldo e-money setelah to up: {self.e_money}")

    def check_operational_hours(self):
        now = datetime.datetime.now().hour
        if 7 <= now < 16:
            return True
        else:
            print("Maaf, aplikasi hanya dapat diakses antara pukul 08:00 hingga 16:00.")
            return False

class Product:
    def __init__(self, idx, name, stock, price, category):
        self.idx = idx
        self.name = name
        self.stock = stock
        self.price = price
        self.category = category

def clear():
    os.system("cls")

# Sample data
products = [
    Product(1, "Original Milk Tea", 26, 24900, "Milk Tea Series"),
    Product(2, "Caramel Milk Tea", 19, 21580, "Milk Tea Series"),
    Product(3, "Hazelnut Milk Tea", 20, 28600, "Milk Tea Series"),
    Product(4, "Black Tea", 29, 22900, "Fresh Tea Series"),
    Product(5, "Green Tea", 37, 20630, "Fresh Tea Series"),
    Product(6, "Boba Milk Tea", 23, 26400, "Fresh Tea Series"),
    Product(7, "Lychee Green Tea", 38, 28500, "Green Tea Series"),
    Product(8, "Peach Green Tea", 19, 26500, "Green Tea Series"),
    Product(9, "Thai Tea", 27, 29500, "Tea Series"),
    Product(10, "Thai Green Tea", 18, 30900, "Tea Series"),
    Product(11, "Lemongrass Tea", 20, 27500, "Tea Series"),
    Product(12, "Lemon Tea", 20, 34000, "Tea Series"),
    Product(13, "Chicken Nugget", 20, 33900, "Snack"),
    Product(14, "French Fries", 20, 35200, "Snack"),
    Product(15, "Sosis Ayam", 30, 28000, "Snack"),
    Product(16, "Chicken Fillet", 25, 35500, "Snack")
]

# Sample usage:
while True:
    print("="*69)
    print("\t\t\tCAFE TEA TIME")
    print("Menu Pembeli hanya dapat diakses antara pukul 08:00 hingga 16:00.")
    print("="*69)
    user_type = input('''
Login sebagai :
[1] Admin
[2] Pembeli 
[3] Keluar
Masukkan pilihan (1/2/3): ''')

    if user_type == "1":
        print("")
        username = input("Username: ")
        password = pwinput.pwinput("PIN: ")
        if username == "admin" and password == "pass":
            admin = Admin(username, password, 35, 'male', '1234')
            print("\nSelamat datang,", username)
            while True:
                print("")
                print("="*50)
                print("\t\tMENU ADMIN")
                print("="*50)
                print("[1] Tambah Makanan/Minuman")
                print("[2] Hapus Makanan/Minuman")
                print("[3] Lihat Semua Daftar Menu Makanan/Minuman")
                print("[4] Kembali ke menu utama")
                choice = input("Pilih menu (1/2/3/4): ")
                if choice == "1":
                    admin.add_product(products)
                elif choice == "2":
                    admin.remove_product(products)
                elif choice == "3":
                    admin.view_products(products)
                elif choice == "4":
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
        else:
            print("Username atau password salah.")
    
    elif user_type == "2":
        print("")
        username = input("Username: ")
        password = pwinput.pwinput("PIN: ")
        # Contoh data pembeli
        buyer_data = {
            "aqiyah": {"age": 19, "gender": "female", "pin": "7777", "e_money": 200000}, #remaja perempuan
            "purnomo": {"age": 55, "gender": "male", "pin": "9999", "e_money": 390000}, #bapak
            "marwani": {"age": 59, "gender": "famale", "pin": "8888", "e_money": 295000}, #ibu
            "valencia": {"age": 13, "gender": "famale", "pin": "0000", "e_money": 290000}, #anak perempuan
            "kevin": {"age": 10, "gender": "male", "pin": "1111", "e_money": 299000} #anak laki2
        }

        if username in buyer_data and password == buyer_data[username]["pin"]:
            buyer_info = buyer_data[username]
            buyer = Buyer(username, password, buyer_info["age"], buyer_info["gender"], buyer_info["pin"], buyer_info["e_money"])
            if buyer.check_operational_hours():
                buyer.greet_user()
                print("TEA TIME")
                print("GREAT TEA GREAT DAY!!!")
                print("PROMO!! Pembelian di atas 100k mendapat diskon 15% dan di atas 350k mendapat diskon 25%")
                while True:
                    print("")
                    print("="*50)
                    print("\t\tMENU PEMBELI")
                    print("="*50)
                    print("[1] Daftar menu makanan dan minuman")
                    print("[2] Top up e-money")
                    print("[3] Kembali ke menu utama")
                    choice = input("Pilih menu (1/2/3): ")
                    if choice == "1":
                        buyer.buy_product(products)
                    elif choice == "2":
                        buyer.top_up_emoney()
                    elif choice == "3":
                        break
                    else:
                        print("Pilihan tidak valid, coba lagi.")
        else:
            print("Username atau password salah.")
    
    elif user_type == "3":
        print("Terima kasih telah menggunakan layanan kami.")
        break
    
    else:
        print("Pilihan tidak valid, coba lagi.")
