# Course5

Markup :  ## Step 1 ##

The data from the given link was scraped using Markup :  _BeautifulSoup4_

The given features were extracted and the data was cleaned.

This is done in the file Markup :  step1.py

Markup :  ## Step 2 ##

Now a json file was generated in step1 which was imported in mongodb database using the following cmd:
Markup :  _mongoimport --db test --collection productreviews --file data.json_

Markup : ![picture alt](https://github.com/mercury297/Course5/blob/master/db_ss.PNG)

Markup :  ## Step 3 ##

Text classification of 1st 100 reviews using Markup :  _Latent Dirichlet Allocation algorithm_

The text is lemmatized, the stop words are removed.

Now the TF-IDF of the text is taken along with LDA model from _nltk library_

Thus we get what topics might be associated with the given text.

More training would yield better results

Markup : ![picture alt](https://github.com/mercury297/Course5/blob/master/lda_model.PNG)

Markup :  ## Step 3 ##

Now finally the semantic analysis is done using _Afinn library_

This does not yield the best results. But due to the time constraint i've used this

Markup : ![picture alt](https://github.com/mercury297/Course5/blob/master/semantic_analysis.PNG)




