import re
import string
import emoji

from nltk.corpus import stopwords as nltk_stopwords
from nltk.tokenize import word_tokenize

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Slang dictionary
slang_dict = {
    # NEGATION
    "g": "tidak",
    "ga": "tidak",
    "gak": "tidak",
    "gk": "tidak",
    "ngga": "tidak",
    "nga": "tidak",
    "nggak": "tidak",
    "enggak": "tidak",
    "ngak": "tidak",
    "ngk": "tidak",
    "tdk": "tidak",
    "kaga": "tidak",
    "kagak": "tidak",
    "tidaak": "tidak",
    "tidka": "tidak",

    # NEGATIVE EXPRESSIONS
    "gabisa": "tidak bisa",
    "gbisa": "tidak bisa",
    "gbs": "tidak bisa",
    "gaje": "tidak jelas",
    "gjls": "tidak jelas",
    "gj": "tidak jelas",
    "gjelas": "tidak jelas",
    "gajelas": "tidak jelas",
    "gada": "tidak ada",
    "gaada": "tidak ada",
    "gtw": "tidak tau",
    "habisa": "tidak bisa",
    "gatau": "tidak tau",

    # APPLICATION / TECH
    "apk": "aplikasi",
    "apl": "aplikasi",
    "apps": "aplikasi",
    "app": "aplikasi",
    "apknya": "aplikasinya",
    "eror": "error",
    "ban": "suspend",
    "suspend": "ditangguhkan",
    "pfp": "foto profil",
    "dm": "direct message",

    # PRONOUN
    "ak": "aku",
    "sy": "aku",
    "sya": "aku",
    "gw": "aku",
    "gua": "aku",
    "gue": "aku",
    "lu": "kamu",
    "lo": "kamu",

    # EMPHASIS
    "bgt": "banget",
    "bgtt": "banget",
    "bngt": "banget",
    "bnget": "banget",
    "bbget": "banget",
    "bngtt": "banget",

    # COMMON WORDS
    "yg": "yang",
    "pake": "pakai",
    "make": "pakai",
    "kalo": "kalau",
    "klo": "kalau",
    "tp": "tapi",
    "tpi": "tapi",
    "ttp": "tetapi",
    "udh": "sudah",
    "udah": "sudah",
    "uda": "sudah",
    "sdh": "sudah",
    "sdah": "sudah",
    "blm": "belum",
    "skrg": "sekarang",
    "skrng": "sekarang",
    "lg": "lagi",
    "lgi": "lagi",
    "dlu": "dulu",
    "bener": "benar",
    "karna": "karena",
    "krna": "karena",
    "ilang": "hilang",
    "jls": "jelas",
    "knp": "kenapa",
    "knpa": "kenapa",
    "ngapa": "kenapa",
    "napa": "kenapa",
    "pdhl": "padahal",
    "trus": "terus",
    "trs": "terus",
    "moga": "semoga",
    "jd": "jadi",
    "jdi": "jadi",
    "jg": "juga",
    "bs": "bisa",
    "bsa": "bisa",
    "org": "orang",
    "kasi": "kasih",
    "bgus": "bagus",
    "jgn": "jangan",
    "nyari": "mencari",
    "nyoba": "mencoba",
    "bnyk": "banyak",
    "bnyak": "banyak",
    "burem": "buram",
    "ad": "ada",
    "dr": "dari",
    "dri": "dari",
    "dgn": "dengan",
    "ny": "nya",
    "aj": "saja",
    "aje": "saja",
    "gmn": "bagaimana",
    "gmna": "bagaimana",
    "kluar": "keluar",
    "slalu": "selalu",
    "mkin": "makin",
    "jlek": "jelek",
    "mmuaskan": "memuaskan",
    "mantip": "mantap",
    "mantapu": "mantap",
    "skli": "sekali",
    "kluar²": "keluar keluar",
    "posotif": "positif",
    "hbis": "habis",
    "kebnyakan": "kebanyakan",
    "krn": "karena",
    "apklsi": "aplikasi",
    "dngn": "dengan",
    "hbis": "habis",
    "pdahal": "padahal",
    "kebnyakan": "kebanyakan",
    "dr": "dari",
    "maasnnttap": "mantap",
    "mantab": "mantap",
    "jls": "jelas",
    "turup": "tutup",
    "tmbh": "tambah",
    "bgs": "bagus",
    "amantap": "mantap",
    "ntap": "mantap",
    "gaasik": "tidak asik",
    "jellek": "jelek",
    "jeleek": "jelek",

    # SOCIAL MEDIA TERMS
    "twiter": "twitter",
    "twit": "tweet",
    "twitt": "tweet",
    "twt": "tweet",
    "twet": "tweet",

    # TOXIC WORDS
    "ajg": "anjing",
    "anj": "anjing",
    "anjeng": "anjing"
}

# Import stopwords
important_words = [
    # NEGATION
    "tidak",
    "tak",
    "bukan",
    "belum",
    "jangan",

    # EMPHASIS
    "banget",
    "sangat",
    "sekali",
    "terlalu",
    "lebih",
    "kurang",
    "parah",

    # SYSTEM / FUNCTIONAL
    "bisa",
    "tidak bisa",
    "gagal",
    "error",
    "loading",
    "login",
    "refresh",

    # EMOTION
    "suka",
    "senang",
    "kecewa",
    "kesal",
    "emosi",
    "marah",
    "sedih",

    # SENTIMENT WORDS
    "bagus",
    "jelek",
    "buruk",
    "keren",
    "mantap",
    "lambat",
    "cepat",
    "lama",
    "lemot",
    "ngelag",
    "lag",
    "loading",
    "delay",
    "buffering",

    # TIME / COMPARISON
    "sekarang",
    "dulu",
    "lagi",

    # PLATFORM TERMS
    "twitter",
    "tweet",
    "akun",
    "suspend",
    "ditangguhkan",
]

stopword_list = set(nltk_stopwords.words('indonesian'))
stopword_list = stopword_list - set(important_words)

# Preprocessing function
def case_folding(text):
    text = text.lower()
    return text

def normalize_repeated_characters(text):
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def remove_url(text):
    return re.sub(r'http\S+|www\S+|https\S+', '', text)

def remove_mention_hashtag(text):
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    return text

def remove_emoji(text):
    return emoji.replace_emoji(text, replace='')

def remove_numbers(text):
    return re.sub(r'\d+', '', text)

def remove_punctuation(text):
    return re.sub(
        f"[{re.escape(string.punctuation)}]",
        " ",
        text
    )
    
def remove_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text)

def tokenize(text):
    return word_tokenize(text)

def normalize_slang(tokens):
    normalized = []
    for word in tokens:
        normalized.append(
            slang_dict.get(word, word)
        )
    return normalized

def remove_stopwords(tokens):
    filtered_tokens = []
    for token in tokens:
        if not token or not token.strip():
            continue
        if token not in stopword_list:
            filtered_tokens.append(token)
    return filtered_tokens

# Main preprocessing function
def preprocess_text(text):
    text = case_folding(text)
    text = normalize_repeated_characters(text)
    text = remove_url(text)
    text = remove_mention_hashtag(text)
    text = remove_emoji(text)
    text = remove_numbers(text)
    text = remove_punctuation(text)
    text = remove_multiple_spaces(text)
    tokens = tokenize(text)
    tokens = normalize_slang(tokens)
    tokens = remove_stopwords(tokens)
    tokens = [
        token
        for token in tokens
        if len(token) > 1
    ]
    return ' '.join(tokens)

