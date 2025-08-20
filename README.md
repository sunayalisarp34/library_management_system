<h1>Kütüphane Yönetim Sİstemi Projesi</h1>

<p>Bu proje üç farklı klasörden oluşur</p>

<ol>
    <li>Aşama 1: Komut Satırı Uygulaması</li>
    <li>Aşama 2: Komut Satırı Uygulaması - API ile zenginleştirilmiş</li>
    <li>Aşama 3: FastAPI Tabanlı Uygulama</li>
</ol>

<p><strong>Proje Amacı:</strong> Kullanıcıların girecekleri bilgi sonrası ilgili dosyaya (library.json) kitaplarını kaydetmelerini sağlamak.</p>

<h1>PROJE HAKKINDA GENEL BİLGİLER</h1>

<p>Projeyi kendi ortamınızda çalıştırmak için reponun sağ ustünde bulunann butondan doğrudan .zip uzantılı bir dosyaya sıkıştırılmış olarak indirebilir ya da<p>

<pre>
git clone https://github.com/sunayalisarp34/library_management_system.git
</pre>

<p>yukarıdaki komutu Git CLI üzerinden girerek kendi ortamınızdaki istediğiniz bir dizine ekleyeblirsiniz.</p>

<h2>Komut Satırı Uygulaması</h2>

<h3>Kurulum ve çalıştırma<h3>

<p>Bu uygulamayı kullanmak için <strong>asama1_cli_app</strong> adlı klasörde komut satırını açıp öncesinde: </p>

```
pip install -r requirements.txt

```
<p>komutunu çalıştırdıktan sonra</p>

```
python main.py
```

<p>komutunu çalıştırmanız gerekmektedir.</p>

<h2>Komut Satırı Uygulaması - API ile zenginleştirilmiş</h2>

<h3>Kurulum ve çalıştırma<h3>

<p>Bu uygulamayı kullanmak için <strong>asama2_cli_app_v2</strong> adlı klasörde komut satırını açıp öncesinde: </p>

```
pip install -r requirements.txt

```
<p>komutunu çalıştırdıktan sonra</p>

```
python main.py
```

<p>komutunu çalıştırmanız gerekmektedir.</p>



<h2>FastAPI Tabanlı Uygulama</h2>

<h3>Kurulum ve çalıştırma<h3>

<p>Bu uygulamayı kullanmak için <strong>asama3_web_api</strong> adlı klasörde komut satırını açıp öncesinde:</p>

```
pip install -r requirements.txt

```
<p>komutunu çalıştırdıktan sonra</p>

```
uvicorn api:app --reload

```

<p>veya</p>

<pre>
fastapi dev api.py
</pre>

<p>veya</p>

<pre>
fastapi run
</pre>

<p>komutlarından birini çalıştırmanız gerekmektedir.</p>