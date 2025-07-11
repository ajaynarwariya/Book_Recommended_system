from flask import Flask , render_template , request
import pickle
import numpy as np
import pandas as pd

popular_df =pickle.load(open("popular.pkl","rb"))
pt = pickle.load(open("pt.pkl","rb"))
books = pickle.load(open("books.pkl","rb"))
similarity_score = pickle.load(open("similarity_score.pkl","rb"))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title']),
                           author= list(popular_df['Book-Author']),
                           image=list(popular_df['Image-URL-M']),
                           votes=list(popular_df['nums_rating']),
                           rating=list(popular_df['avg_rating']),


                           )
@app.route("/recommend")
def recommend():
    return render_template('recommend.html')

@app.route("/recommend_books", methods=['POST'])
def recommend_books():
    user_input = request.form.get("user_input")

    # fetch index
    index = np.where(pt.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_item:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('recommend.html', data = data)


if __name__ == "__main__":
    app.run(debug=True)