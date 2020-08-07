import string
import re
import nltk
import emoji
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


def normalize(text):
    # Remove emojis
    text = emoji.get_emoji_regexp().sub(u'', text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove the punctuations
    tokens = [word.translate(str.maketrans(
        '', '', string.punctuation)) for word in tokens]
    # Lower the tokens
    tokens = [word.lower() for word in tokens]
    # Remove stopword
    tokens = [
        word for word in tokens if not word in stopwords.words("turkish")]
    # Remove multiple spaces in the sentence
    value = re.sub(' +', ' ', ' '.join(tokens))
    # Remove any leading and trailing whitespaces
    value = str.strip(value)
    return value


if __name__ == "__main__":
    sentences = [
        "İstediğim renkte gelmedi. Kalitesi de resimdeki gibi iyi değil. Bu fiyata bu çanta fazla..",
        "Parmak arası sandaletlerin en rahatı, en şıkı🙏     ayakta yok hissi. Diğer renklerini de alacağım. Şiddetle tavsiye edilir. Teşekkürler Oblavion ve Trendyol.",
        "muhteşem ötesi. yumuşacık rahat ve çok şık bir sandalet. bir numara büyük tercih edilmeli😊",
        "tam alacakken indirim kalktı kısa zamanda yine indirim bekliyorum 🤗",
        "    abc    ",
        "Aynı özellikte neredeyse iki katı paraya isim yapmış marka almaya lüzum yok. Kaliteli ve ucuz. Smart tv özelliği yok ama Xioami mi tv box aldım, smart tvlerden on kat daha iyi. Kesinlikle tavsiye ederim.",
        "Ürünü yaklaşık iki aydır kullanıyorum. Daha doğrusu kullanmaya çalışıyorum. Kulaklıklardan biri diğerini görmüyor. Bir kez servise gitti. Şuan yine aynı problemi yaşıyorum. Kesinlikle tavsiye etmiyorum.",
        "Üründe çok ciddi bir gecikme sıkıntısı var. Bazen 1 saniyelere kadar çıkıyor. Bazense hissedilmeyecek kadar azalıyor ama çok nadir. Onun dışında ses kalitesini gerçekten beğenmedim. 40 liralık başka bir kulaklık ile karşılaştırdığımda bariz bir şekilde kötü. Sesler tenekeden geliyor gibi. Çok uzun saatler kulaklıkla müzik dinleyen ben bununla yarım saatte baş ağrısından bırakıyorum. Bilgisayardan kullanmak gibi bir niyetiniz varsa ayrıca uzak durun. Bağlanıyor direk ancak ses alma konusunda tam bir fiyasko. Bağlı olmasına rağmen ses alabilmek için her seferinde en az 15 dk bununla uğraştım. Zaten geç gelen kalitesiz bir ses var onu bile düzenli alamıyorsunuz 3-5 dkda bir ses yarım saniyeliğine bir saniyeliğine kesiliyor. Sürekli ne oldu diyerek tetikte bekliyorsunuz. Onun dışında tasarım olarak başarılı. Kutusu gayet taşınabilir ve şık. Şarj konusunda birşey diyemiyorum çünkü çok çektirdi kullanamadım.",
        "Teslimat çok hızlı ve sorunsuz oldu, bunun için teşekkür ederim. Ürünün kalitesi beklentileri karşılıyor. Kullanımı çok kolay. Bağlantı veya konuşmada sorun yaşamadım. Kulak içinde durması için gönderilen yedek aparat silikonlarla rahat ettiğimi söyleyebilirim. Sesimin iletilmesinde hiç sorun yaşamadım. Müzik dinlerken dışardan gelen sesleri çok kapatamıyor ancak açıkcası bunu çok da istemiyorum çünkü yolda yürürken müzik dinlerken tamamen izole olmak oluşabilecek bir tehlikeyi fark edememek beni tedirgin ediyor. Sesi biraz daha açıp dış seslerden gelen etkiyi azaltmak mümkün. Tek eksiği ses ayarının telefonda yapılabilir olması. Bu fiyat için uygun bir ürün bence.",
        "anne ve babam için almıştım. Kablotv seyrediyorlar. Kurulum kolay oldu.Beklentilerini fazlasıyla karşıladı. Görüntü kalitesi güzel. Pahalı tv almaya gerek görmedik. Doğru tercih yapmışız."
    ]
    for text in sentences:
        print(f"-> {normalize(text)}")
