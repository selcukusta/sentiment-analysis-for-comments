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
        "Aynı özellikte neredeyse iki katı paraya isim yapmış marka almaya lüzum yok. Kaliteli ve ucuz. Smart tv özelliği yok ama Xioami mi tv box aldım, smart tvlerden on kat daha iyi. Kesinlikle tavsiye ederim."
    ]
    for text in sentences:
        print(normalize(text))
