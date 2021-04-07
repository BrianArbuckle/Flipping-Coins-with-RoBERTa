# Flipping-Coins-with-RoBERTa
### Final project for Stanford XCS224U - Natural Language Understanding 

This paper shows an application of transformer models (RoBERTa) to predict stock market movement. Our research efforts focused on extracting the financial 'sentiment' of stock-price performance by leveraging company filings. We used the SEC data to train our model and used the equal weighted NASDAQ 100 index as our benchmark. Recognizing the strengths of a sentiment classification task, we adopted stock-performance as a proxy for 'sentiment.' This predicted stock outcomes compared to the market index. Our initial success came from removing noise in the form of boilerplate text. Next, we chose logistic regression and the Naive Bayes classification model on smaller data sets with iterative optimization for the testing model. Finally, we ran our original system with RoBERTa for stock price performance 'sentiment' predictions. We found that transformer and traditional machine learning approaches produced suboptimal results that are on par with a random guess, which is why we included our cheeky coin toss results. The real challenge, as our research confirmed, came from the sentiment free tone used in the company filings.

To work with the parsed data and cleaned dataframes, [download the pickle_data folder](https://www.dropbox.com/s/ah8ds55r6ktguaz/pickle_data.zip?dl=1), and place the folder in the same directory as the notebooks. Also, the contents of the `src` folder should be in the same folder as the notebooks, so the utility functions are available to the notebooks from the `.py` files.

To build the docker container, `cd` into the docker folder and run (be sure to include the period at the end):

```bash
docker build -t jupyter/stanford-final .
```
Then `cd` into the main project directory "Flipping-Coins-with-RoBERTa" and run the following to launch the container:

```bash
docker run --rm -p 8888:8888 -v "$PWD":/home/jovyan/work jupyter/stanford-final
```
