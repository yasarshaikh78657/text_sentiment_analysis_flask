import requests
from flask import Flask,render_template, redirect, request
import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


app = Flask(__name__)


@app.route('/')
def index():
    return  render_template('index.html',
                                   title='add text '
                                         'and submit')
def analyze_text(var):

    #text = open('read.txt', encoding='utf-8').read()
    lower_case = var.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

    # Using word_tokenize because it's faster than split()
    tokenized_words = word_tokenize(cleaned_text, "english")

    # Removing Stop Words
    final_words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)

    # Lemmatization - From plural to single + Base form of a word (example better-> good)
    lemma_words = []
    for word in final_words:
        word = WordNetLemmatizer().lemmatize(word)
        lemma_words.append(word)

    emotion_list = []
    with open('emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')

            if word in lemma_words:
                emotion_list.append(emotion)

    print(emotion_list)
    w = Counter(emotion_list)
    print(w)


    def sentiment_analyse(sentiment_text):
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        if score['neg'] > score['pos']:
            ans = "Negative Sentiment"
        elif score['neg'] < score['pos']:
            ans = "Positive Sentiment"
        else:
            ans = "Neutral Sentiment"
        return ans


    result = sentiment_analyse(cleaned_text)
    return result,emotion_list,w
    

										 


@app.route('/fetch', methods=['POST'])
def fetch():
    var = request.form["txt"]
    strres = analyze_text(str(var))

    return render_template('fetch.html', strres= strres )

if __name__ == "__main__":
    app.run(debug=True)


###function to run for prediction
##def detecting_fake_news(var):    
##  #retrieving the best model for prediction call
##  prediction = load_model.predict([var])
##  prob = load_model.predict_proba([var])
##  stc = "The given proclamation is {} reality probability score is {}"
##  stc = stc.format(prediction[0],prob[0][1])
##  if stc=="The given proclamation is True reality probability score is 0.6828804214017451":
##      stc="Invalid text"
##      return stc
##  else:
##      return stc
