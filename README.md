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

## KULLANIM (_[Fixy-TR](https://github.com/Fixy-TR/fixy) tarafından sağlanan veri seti ile_)

[Fixy-TR](https://github.com/Fixy-TR/fixy/blob/master/data/sentiment_data.csv) tarafından açık kaynaklı sağlanan veri seti `/dataset/sentiment_data.csv` içerisinde yer almaktadır.

`python3 prepare_data.py` komutu ile **FastText** tarafından yorumlanabilir etiketlerle `/dataset/comments.train` dosyası tekrar oluşturulabilir.

`comments.train` _(281,461 yorum)_ dosyasındaki `__label__(positive|negative)` etiketleri, `sentiment_data.csv` dosyasındaki `Rating` kolonundaki değere göre belirlenmiştir. **1.0** puan `positive`, **0.0** puan ise `negative` olarak kabul edilmiştir.

#### Model oluşturma

`/dataset/comments.train` dosyası kullanılarak tasnif modeli oluşturulur. Bunun için `fasttext supervised -input comments.train -output model_comments -epoch 25 -lr 1.0 -wordNgrams 3` komutunun çalıştırılması yeterlidir. `epoch`, `lr (learning rate)` ve `wordNGrams` parametreleri ile modelin öğrenme yetkinliği arttırılabilir/azaltılabilir.

#### Modeli test etme

Üretilmiş tasnif modeli, daha önce doğruluğu kanıtlanmış sonuçlar yardımıyla test edilebilir. `/dataset/comments.valid` dosyası bu test işlemi için kullanılacaktır. **Önerilen yöntem, test dosyalarındaki içeriklerin insani yetkinliklerle etiketlenmesidir.**

`fasttext test fastText/model_comments.bin fastText/comments.valid` komutu ile test çalıştırılır ve aşağıdaki gibi bir sonuç beklenir:

```
N       387
P@1     0.943
R@1     0.943
```

Yukarıdaki tablo, tasnif modeli doğrultusunda yapılan etiket tahmininin %94.3 doğru olduğunu ifade ediyor.

#### Girilen değerin tahminlenmesi

`fasttext predict fastText/model_comments.bin -` komutu ile de komut istemcisinden girilen değerin anlık olarak tahminlenmesini sağlayabiliriz. Aşağıdaki örnekler internetten alınan gerçek kullanıcı yorumlarıdır:

| YORUM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | TAHMİN              |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| _teslimat hızlı sorunsuz oldu bunun teşekkür ederim ürünün kalitesi beklentileri karşılıyor kullanımı kolay bağlantı konuşmada sorun yaşamadım kulak içinde durması gönderilen yedek aparat silikonlarla rahat ettiğimi söyleyebilirim sesimin iletilmesinde sorun yaşamadım müzik dinlerken dışardan gelen sesleri kapatamıyor ancak açıkcası bunu istemiyorum yolda yürürken müzik dinlerken tamamen izole olmak oluşabilecek bir tehlikeyi fark edememek beni tedirgin ediyor sesi biraz açıp dış seslerden gelen etkiyi azaltmak mümkün tek eksiği ses ayarının telefonda yapılabilir olması fiyat uygun bir ürün bence_                                                                                                                                                                                                                                      | `__label__positive` |
| _üründe ciddi bir gecikme sıkıntısı var bazen 1 saniyelere kadar çıkıyor bazense hissedilmeyecek kadar azalıyor nadir onun dışında ses kalitesini gerçekten beğenmedim 40 liralık başka bir kulaklık karşılaştırdığımda bariz bir şekilde kötü sesler tenekeden geliyor uzun saatler kulaklıkla müzik dinleyen ben bununla yarım saatte baş ağrısından bırakıyorum bilgisayardan kullanmak bir niyetiniz varsa ayrıca uzak durun bağlanıyor direk ancak ses alma konusunda tam bir fiyasko bağlı olmasına rağmen ses alabilmek seferinde 15 dk bununla uğraştım zaten geç gelen kalitesiz bir ses var onu bile düzenli alamıyorsunuz 35 dkda bir ses yarım saniyeliğine bir saniyeliğine kesiliyor sürekli oldu diyerek tetikte bekliyorsunuz onun dışında tasarım olarak başarılı kutusu gayet taşınabilir şık şarj konusunda diyemiyorum çektirdi kullanamadım_ | `__label__negative` |
| _2 günde kırıldı_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `__label__negative` |
| _ürünün desenleri açılıyor boyunu kisaltim iade oluyorsa iade edecem_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `__label__negative` |
| _bilmiyorum ama sanki iyidir idare der_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `__label__positive` |
| _anne babam almıştım kablotv seyrediyorlar kurulum kolay oldubeklentilerini fazlasıyla karşıladı görüntü kalitesi güzel pahalı tv almaya gerek görmedik doğru tercih yapmışız_                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `__label__positive` |

## REFERANSLAR

- https://fasttext.cc/docs/en/supervised-tutorial.html
- https://github.com/Fixy-TR/fixy
