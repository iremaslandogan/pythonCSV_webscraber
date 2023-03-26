# Kitap Bilgileri Tamamlayıcı
Bu CLI uygulaması, kullanıcının kişisel kitap listesindeki eksik bilgileri tamamlamasına yardımcı olmak için tasarlanmıştır. Uygulama, belirtilen kaynak siteleri kullanarak verileri web kazıma yöntemiyle toplar ve CSV dosyasındaki eksik alanları doldurur.

Kurulum
Git deposunu yerel bilgisayarınıza kopyalayın veya zip dosyasını indirin.
Ana dizindeki requirements.txt dosyasında belirtilen kütüphaneleri yüklemek için aşağıdaki komutu kullanın:
```bash
pip install -r requirements.txt
```
Kullanım
```bash
python app.py 
```
Program çalıştıktan sonra başlangıç, bitiş ve hangi değer ile arama yapmak istiyorsanız seçim yapmalısınz.

Test Kullanım
```bash
python unittest.py 
```
Docker Kullanım

docker build komutunu kullanarak Docker imajını derleyebilirsiniz. Aşağıdaki komut Dockerfile'ı kullanarak csvscraper adlı bir imaj oluşturur
```bash
docker build -t csvscraper .
```
Docker imajını başlatmak için docker run komutunu kullanabilirsiniz. Aşağıdaki komut, csvscraper adlı Docker imajını çalıştırır

```bash
docker run -it csvscraper
```
Örnek Program Çıktısı
```bash
Please enter initial index: 0
Please enter the ending index: 5
Please make your selection:
1 - Title
2 - ISBN
1
Number of remaining searches:  2
Number of Writing Data:  1
No search results found: Dine Karsi Din
Number of remaining searches:  1
Number of Writing Data:  1
No search results found: Semaver
Number of remaining searches:  0
Number of Writing Data:  1
```

