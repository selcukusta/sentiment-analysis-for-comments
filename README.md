# ÜRÜN YORUMLARINDAN DUYGU ANALİZİ (SENTIMENT ANALYSIS)

## AMAÇ

Facebook Research ekibi tarafından aktif olarak geliştirilen `FastText` ürünü ile, e-ticaret sitesinden çekilen ürün yorumları üzerine duygu analizi gerçekleştirmek.

Büyük ölçekli bir projede modül olarak planlanan bir fikrin deneysel uygulamasıdır.

## KURULUM

- Python 3
- `pip install -r requirements.txt`
- [FastText](https://fasttext.cc/docs/en/support.html)

## KULLANIM

Hali hazırda `/products` klasörü altında [Trendyol](https://www.trendyol.com/) üzerinden satış yapan 2 farklı satıcıya ait ürünlerin listesi ve `/fastText` klasörü altında bu ürünlere ait yorumların etiketlenmiş hali bulunmaktadır.

`comments.train` _(98,649 yorum)_ ve `comments.valid` _(387 yorum)_ dosyalarındaki `__label__(positive|negative|notr)` etiketleri, tüketicilerin ürüne verdikleri puana _(1-5)_ göre belirlenmiştir. **1, 2** puan `negative`, **3** puan `notr`, **4, 5** puan ise `positive` olarak kabul edilmiştir.

Değerlendirme aralıklarını `comments.py` dosyasındaki **66.-71.** satırları arasından değiştirebilirsiniz.

_**NOT:** Değerlendirme aralıkları değiştikten sonra `.train` ve `.valid` dosyaları tekrar üretilmelidir. Bu esnada gerçekleşecek web crawling işleminde, hem kaynak siteye zarar vermemek hem de threshold'a (belirli süre içerisinde yapılacak istek sınırı) takılmamak için iki istek arasında belirli bir süre beklenmelidir. Varsayılan 3 saniyedir._

#### Model oluşturma

`/fastText/comments.train` dosyası kullanılarak tasnif modeli oluşturulur. Bunun için `fasttext supervised -input fastText/comments.train -output fastText/model_comments -epoch 20 -lr 1.0 -wordNgrams 3` komutunun çalıştırılması yeterlidir. `epoch`, `lr (learning rate)` ve `wordNGrams` parametreleri ile modelin öğrenme yetkinliği arttırılabilir/azaltılabilir.

#### Modeli test etme

Üretilmiş tasnif modeli, daha önce doğruluğu kanıtlanmış sonuçlar yardımıyla test edilebilir. `/fastText/comments.valid` dosyası bu test işlemi için kullanılacaktır. **Önerilen yöntem, test dosyalarındaki içeriklerin insani yetkinliklerle etiketlenmesidir.**

`fasttext test fastText/model_comments.bin fastText/comments.valid` komutu ile test çalıştırılır ve aşağıdaki gibi bir sonuç beklenir:

```
N       387
P@1     0.915
R@1     0.915
```

Yukarıdaki tablo, tasnif modeli doğrultusunda yapılan etiket tahmininin %91.5 doğru olduğunu ifade ediyor.

#### Girilen değerin tahminlenmesi

`fasttext predict fastText/model_comments.bin -` komutu ile de komut istemcisinden girilen değerin anlık olarak tahminlenmesini sağlayabiliriz. Aşağıdaki örnekler internetten alınan gerçek kullanıcı yorumlarıdır:

| YORUM                                                                                                                                                                                                                                | PUAN (1-5) | TAHMİN                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | --------------------- |
| _ürün çok kalitesiz çerçeve berbat çözünürlük idare eder_                                                                                                                                                                            | **1**      | `__label__negative`   |
| _39 giyen biri olarak bazi yorumlarda bir numara büyük alınması tavsiye ediliyordu ayakkabının biraz sert bir kalıbı olduğunu bildiğim için 39 numarayı tereddütle aldım tam ve rahat oldu iyiki 40 almamışım bence numaranızı alın_ | **5**      | `__label__positive`   |
| _2 günde kırıldı_                                                                                                                                                                                                                    | **1**      | `__label__negative`   |
| _ürünün desenleri açılıyor boyunu kisaltim iade oluyorsa iade edecem_                                                                                                                                                                | **1**      | `__label__negative`   |
| _bilmiyorum ama sanki iyidir idare der_                                                                                                                                                                                              | **3**      | `__label__notr`       |
| _anne ve babam için almıştım. Kablotv seyrediyorlar. Kurulum kolay oldu.Beklentilerini fazlasıyla karşıladı. Görüntü kalitesi güzel. Pahalı tv almaya gerek görmedik. Doğru tercih yapmışız._                                        | **5**      | `__label__positive__` |

## REFERANSLAR

- https://fasttext.cc/docs/en/supervised-tutorial.html
