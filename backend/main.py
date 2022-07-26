from pydantic import BaseModel
from fastapi import FastAPI
from epitran.backoff import Backoff
from fastapi.middleware.cors import CORSMiddleware
import enum

app = FastAPI()

""" Yes, I know. One should not do this - Ever. """
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

languages = [
        {
            "id" : 1,
            "iso": "deu-Latn",
            "label": "German (Deutsch)"
        },
        {
            "id" : 2,
            "iso": "eng-Latn",
            "label": "English"
        },
        {
            "id" : 3,
            "iso": "fra-Latn",
            "label": "French (Français)"
        },
        {
            "id": 4,
            "iso": "ita-Latn",
            "label": "Italian (Italiano)"
        },
    ]

class TransliterationTypes(str, enum.Enum):
    IPA = "IPA"
    X_SAMPA = "X-SAMPA"

class Language(BaseModel):
    id: int
    iso: str
    label: str

class Text(BaseModel):
    native_text: str

""" returns all languages from list above """
@app.get("/languages", response_model=list[Language])
def read_languages(): 
    return languages

""" returns transliteration of given text """
@app.post("/transliterate/{lang_id}")
def write_transliteration(lang_id: int, transliteration_type: TransliterationTypes, text: Text):
    sought_lang: Language = None

    """ find given language in language list above """
    for lang in languages:
        if lang['id'] == lang_id:
            sought_lang = lang

    """ transliterate using known language and given transliteration type """
    if sought_lang:
        backoff = Backoff([sought_lang["iso"], "eng-Latn"])

        words = extract_words(text.native_text)

        transliterated_text = ""
        for word in words:

            if words[words.__len__()-1] == word:
                transliterated_text += transliterate_word(transliteration_type, word, backoff)

            else:
                transliterated_text += transliterate_word(transliteration_type, word, backoff) + " "
        
        return transliterated_text
        
    return {"Message": "There is no Language with this ID"}

""" returns a list of words that are stripped of special characters """
def extract_words(text: str):
    no_special_text = ""
    for char in text:
        if char.isalnum() or char.isspace():
            no_special_text += char

    return no_special_text.split()

""" returns transliteration of a given word using a given transliteration type and epitran backoff instance """
def transliterate_word(transliteration_type: TransliterationTypes, word: str, backoff):
    transliterated_word = ""
    
    if transliteration_type == TransliterationTypes.X_SAMPA:
        xsampa_list = backoff.xsampa_list(word)
        for phenom in xsampa_list:
            transliterated_word += phenom
    else:
        transliterated_word += backoff.transliterate(word)

    return transliterated_word
