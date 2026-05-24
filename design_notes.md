\# Bölüm 2: Turing Makineleri Tasarım Notları



\## TM-1: Unary → Binary Çevirici (`unary\_to\_binary.yaml`)

\*\*1. Strateji:\*\* Algoritma üç ana aşamadan oluşuyor. Önce tekli (unary) sayıdaki '1'leri soldan sağa teker teker 'X' ile işaretledim. Her işaretlemede şeridin en sağına giderek orada "ters" bir ikili sayacı artırdım. Tüm 1'ler bitince X'leri sildim. Son aşamada ise tersten oluşan bu ikili sayıyı, matematiksel olarak doğru formata getirmek için ters çevirdim (reverse işlemi).

\*\*2. Durum Sayısı:\*\* Toplam 19 durum kullandım. Ters çevirme (reverse) algoritması biraz karmaşık olduğu için durum sayısı arttı. Taşıma (carry) işlemleri için durumları birleştirebilirdim ama modülerliği bozmamak adına ayrı tuttum.

\*\*3. Şerit Alfabesi:\*\* `{1, 0, B, X}` kullandım. 'X' sembolünü işlediğim 1'leri işaretlemek için kullandım. Başka bir işaretleyiciye gerek kalmadı.

\*\*4. Karmaşıklık:\*\* Girdi uzunluğu $n$ iken, her 1 için şeridin sonuna gidip dönüldüğü için $O(n^2)$ adım sürer.

\*\*5. Hata Ayıklama:\*\* En çok ters çevirme (reverse) aşamasında zorlandım. Binary stringi yerinde ters çevirmeye çalışırken karakterleri ezdiğimi fark ettim. Çözüm olarak araya bir X koyup karakterleri onun soluna "taşıyarak" sorunu çözdüm.



\## TM-2: İki İkili Sayıyı Karşılaştıran TM (`binary\_compare.yaml`)

\*\*1. Strateji:\*\* $A > B$ kontrolü yapmam gerekiyordu. Önce iki sayının uzunluğunu karşılaştırdım. Bir sayının rakamını X veya Y yapıp karşılığını aradım. Eğer A'da hala rakam varken B bittiyse (A > B) doğrudan kabul ettim. Uzunluklar eşit çıkarsa, şeridin başına dönüp karakter karakter soldan sağa değer kontrolü yaptım (A'da 1, B'de 0 bulursam kabul).

\*\*2. Durum Sayısı:\*\* 23 durum kullandım. Karşılaştırma için A ile B arasında sürekli git-gel yapıldığı için durum sayısı fazla oldu. Daha az durum mümkün değildi çünkü çoklu şerit (multi-tape) kullanamıyoruz.

\*\*3. Şerit Alfabesi:\*\* `{0, 1, #, X, Y, B, s}`. 0'ı okuduğumu hatırlamak için X, 1'i hatırlamak için Y kullandım. 's' ise işlenmiş kısımları atlamak için.

\*\*4. Karmaşıklık:\*\* Uzunluk ve değer kontrolü için sürekli baştan sona tarama yapıldığından karmaşıklık $O(n^2)$ olur.

\*\*5. Hata Ayıklama:\*\* En büyük "bug" mantıksal bir hataydı. Kılavuzu yanlış yorumlayıp ilk başta "İki sayı eşit mi?" (A == B) kontrolü yapan bir makine tasarlamıştım. Tüm kodları yazdıktan sonra şartnamenin $A > B$ olduğunu fark edip makinenin tüm mantığını (önce uzunluk, sonra değer kontrolü yapacak şekilde) sil baştan değiştirmek zorunda kaldım.



\## TM-3: Dizgi Kopyalayıcı (`string\_copy.yaml`)

\*\*1. Strateji:\*\* Girdinin sonuna önce '#' eklenir. Ardından ilk işaretlenmemiş karakter okunur (a ise A, b ise B' yapılır). Şeridin en sağındaki boşluğa (B) gidilip o karakter yazılır. Sola geri dönülür ve bu işlem tüm karakterler bitene kadar tekrarlanır. En son A'lar a'ya, B'ler b'ye dönüştürülüp temizlenir.

\*\*2. Durum Sayısı:\*\* Sadece 8 durum kullandım. Girdi alfabesi küçük olduğu için çok kompakt bir çözüm oldu.

\*\*3. Şerit Alfabesi:\*\* Zorunlu olan `{a, b, B, #, A, B'}` sembollerini kullandım. Büyük harfler okunmuş karakterleri takip etmek için kritikti.

\*\*4. Karmaşıklık:\*\* Her bir karakteri kopyalamak için stringin sonuna kadar gidip dönüldüğü için zaman karmaşıklığı $O(n^2)$'dir.

\*\*5. Hata Ayıklama:\*\* Geri dönüş kısmında (q\_return durumu) ufak bir bug yaşadım. Kopyalanan harfi yazdıktan sonra sola dönerken '#' işaretini görünce durması gerekirken A veya B' işaretlerini arıyordu. Geçiş kuralına `read: "#", next: "q\_return"` ekleyerek sorunu düzelttim.



\## TM-4: 4'e Bölünebilirlik Testi (`student\_choice.yaml`)

\*\*1. Strateji:\*\* İkili (binary) bir sayının 4'e bölünebilmesi için son iki hanesinin "00" olması (veya sayının tek basamaklı "0" olması) yeterlidir. Makine şeridin en sağına kadar gidiyor, ardından bir adım sola gelip son hanenin 0 olup olmadığına, sonra bir adım daha sola gelip önceki hanenin 0 olup olmadığına bakıyor.

\*\*2. Durum Sayısı:\*\* Sadece 3 durumla (q0, q\_check\_last, q\_check\_second\_last) çözdüm. Çözülebilen en optimal yöntem buydu.

\*\*3. Şerit Alfabesi:\*\* Herhangi bir yardımcı işaretleyiciye ihtiyaç duymadım. Sadece temel alfabe `{0, 1, B}` yetti.

\*\*4. Karmaşıklık:\*\* Tüm şeridi sadece bir kez sağa tarayıp 2 adım sola döndüğü için karmaşıklık $O(n)$'dir (Lineer).

\*\*5. Hata Ayıklama:\*\* Başlangıçta algoritmayı "00" ile biten sayılar için tasarladım. Ancak test aşamasında sadece "0" girdisi verildiğinde (ki 4'e kalansız bölünür) makinenin çöküp Reject verdiğini gördüm. Kenar durum (edge case) hatasıydı. `q\_check\_second\_last` durumundayken boşluk (B) okursa kabul durumuna geçmesini sağlayarak bu bug'ı aştım.

