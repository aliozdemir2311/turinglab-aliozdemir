# TuringLab: Tek Şeritli Deterministik Turing Makinesi Simülatörü ve Uygulamaları
**Ders:** Hesaplama Kuramı Final Ödevi  
**Değerlendirme:** Ahmet Erharman  
**Geliştirici:** [Ali Özdemir]  

---

## 1. Giriş
TuringLab projesi, teorik bilgisayar biliminin temel taşlarından biri olan Deterministik Tek Şeritli Turing Makinesi (Deterministic Single-Tape Turing Machine) modelini somut, çalışan ve test edilebilir bir yazılım mimarisine dönüştürmek amacıyla geliştirilmiştir. Proje kapsamında, YAML formatında tanımlanan biçimsel Turing Makinesi (TM) spesifikasyonlarını dinamik olarak ayrıştıran, doğrulayan ve simüle eden bir Python motoru (`tm_engine.py`) sıfırdan inşa edilmiştir. 

Bu motor kullanılarak hesaplama kuramı dersi kazanımları doğrultusunda belirlenmiş 4 farklı problemin (Unary-Binary Çevirici, İkili Sayı Karşılaştırıcı, Dizgi Kopyalayıcı ve 4'e Bölünebilirlik Testi) TM tabanlı çözümleri tasarlanmış ve endüstriyel standartlara uygun `unittest` senaryolarıyla doğrulanmıştır.

---

## 2. Mimari ve Tasarım Kararları
Yazılım mimarisi, Turing Makinesi soyutlamasını modüler bir yapıda yansıtmak adına iki ana bileşen üzerine kurulmuştur: `Tape` (Şerit) ve `TuringMachine` sınıfları.

### Şerit (Tape) Temsili
Turing makinelerinde şerit, teorik olarak her iki yöne doğru sonsuzdur. Gerçek dünya donanım sınırları dahilinde bu sonsuzluğu simüle etmek için **Python Sözlükleri (Dictionary)** veya dinamik olarak genişleyen **Listeler** düşünülmüştür. Bellek yönetimi ve indeksleme kolaylığı açısından, kafa konumuna göre sağa ve sola dinamik olarak genişleyen, okunmayan indeksleri "Blank (B)" karakteriyle dolduran esnek bir veri yapısı tercih edilmiştir. Bu sayede kafa negatif indekslere (`L` yönünde hareket ederken) geçse dahi sistem çökmeyerek teorik modele sadık kalınmıştır.

### Durum Geçişleri (Transitions) Kontrolü
YAML dosyasından okunan kurallar, arama maliyetini minimize etmek amacıyla `(mevcut_durum, okunan_karakter) -> (sonraki_durum, yazılacak_karakter, yön)` şeklinde bir **Hash Map (Sözlük)** yapısında saklanır. Bu tasarım kararı, her adımda (step) geçiş kuralını arama karmaşıklığını $O(1)$ seviyesine indirerek simülatörün performansını optimize etmiştir.

---

## 3. Tasarlanan Turing Makineleri
Proje kapsamında `machines/` dizini altında 4 farklı makine hayata geçirilmiştir:

1. **TM-1 (Unary → Binary Çevirici):** Girdi olarak verilen tekli sayı sistemindeki '1' karakterlerini işaretleyip şeridin sağına binary sayaç ekleyerek çalışır. Yerinde dönüşüm ve bit kaydırma algoritmaları entegre edilmiştir.
2. **TM-2 (İkili Sayı Karşılaştırıcı):** İki binary sayıyı (`A#B`) öncelikle uzunluk, ardından soldan sağa basamak değerlerine göre tarayarak $A > B$ koşulunu test eder.
3. **TM-3 (Dizgi Kopyalayıcı):** Verilen $w$ dizgisini $w\#w$ formatına kopyalar. İşaretleyici büyük harfler (`A`, `B'`) yardımıyla karakter takibi yapılır.
4. **TM-4 (4'e Bölünebilirlik Testi - Öğrenci Seçimi):** İkili sistemdeki bir sayının matematiksel olarak son iki hanesinin `00` (veya doğrudan `0`) olması durumunda kabul durumuna geçen, $O(n)$ lineer zaman karmaşıklığına sahip son derece optimal bir makinedir.

**En Zorlayıcı Makine:** Kesinlikle **TM-2 (Karşılaştırma)** makinesi olmuştur. Tek şerit üzerinde iki farklı sayının büyüklük ilişkisini kontrol etmek, kafanın sürekli olarak `#` ayracının soluna ve sağına gitmesini (ileri-geri tarama) gerektirmiştir. Bu durum durum sayısını (state) 23'e çıkarmış ve çok şeritli (multi-tape) makinelerin yazılım mimarisindeki pratik önemini çok net bir şekilde kavramamı sağlamıştır.

---

## 4. Kavramsal Tartışma: Halting Problemi ve TuringLab
*(Hocanın istediği Seçenek A seçilmiştir)*

**Halting (Durma) problemini TuringLab simülatörü içinde "kesin olarak çözmek" matematiksel ve teorik olarak imkansızdır.** Alan Turing'in 1936 yılında kanıtladığı üzere, herhangi bir Turing makinesinin verilen bir girdi ile sonsuz döngüye mi gireceğini yoksa duracağını (kabul/ret) önceden tahmin edebilecek genel bir algoritma (veya üst bir Turing makinesi) mevcut olamaz. 

TuringLab simülatörümüz, verilen geçiş kurallarını tıkır tıkır çalıştıran bir yürütücüdür. Eğer tasarladığımız bir makine mantıksal bir hatadan ötürü şerit üzerinde sonsuz döngüye girerse (örneğin sürekli sağa gidip karakter değiştirmeden aynı duruma kalırsa), TuringLab motorumuz da o makineyle birlikte sonsuz döngüde kalacaktır. 

Pratik yazılım mühendisliğinde bu durumu engellemek için simülatör motoruna `max_steps=10000` gibi bir **adım sınırı (timeout)** ekleyebiliriz. Ancak bu bir "çözüm" değildir; sadece zoraki bir durdurmadır. Çünkü makinenin 10.001'inci adımda durup durmayacağını asla bilemeyiz. Dolayısıyla Halting problemi, TuringLab mimarisinin bir eksiği değil, hesaplama biliminin evrensel ve matematiksel bir sınırıdır.