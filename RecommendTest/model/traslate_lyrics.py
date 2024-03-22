from googletrans import Translator
import pandas as pd

from data import Session
from model.lyric import Lyric

session = Session()

def get_lyrics_data(session):
    result = session.query(Lyric.en_text).limit(20).all()
    return result

lyric_df = pd.DataFrame(get_lyrics_data(session))
# print(lyric_df)

class Google_Translator:
    def __init__(self):
        self.translator = Translator()
        self.result = {'src_text': '', 'src_lang': '', 'tgt_text': '', 'tgt_lang': ''}

    def translate(self, text, src='en', dest='ko'):
        translated = self.translator.translate(text, src=src, dest=dest)
        self.result['src_text'] = translated.origin
        self.result['src_lang'] = translated.src
        self.result['tgt_text'] = translated.text
        self.result['tgt_lang'] = translated.dest

        return self.result

    def translate_file(self, file_path, lang='en'):
        with open(file_path, 'r') as f:
            text = f.read()
        return self.translate(text, lang)

def translate_lyrics(lyric_df, lang='ko'):
    translator = Google_Translator()
    translated_lyrics = []

    for index, row in lyric_df.iterrows():
        en_text = row['en_text']
        translated_result = translator.translate(en_text, lang)
        translated_lyrics.append((en_text, translated_result['tgt_text']))

    # 번역된 결과를 DataFrame에 추가
    lyric_df['translated_text'] = [translated_text for _, translated_text in translated_lyrics]

    return lyric_df

translated_lyrics_df = translate_lyrics(lyric_df, lang='ko')
for index, row in translated_lyrics_df.iterrows():
    print(f"Original: {row['en_text']}")
    print(f"Translated: {row['translated_text']}")
    print()
