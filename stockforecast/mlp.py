from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import datetime as dt
import yfinance as yf

company = 'AAPL'

# Define a start date and End Date
start = dt.datetime(2010,5,12)
end =  dt.datetime(2023,5,12)

# Read Stock Price Data 
df = yf.download(company, start , end)
df["Diff"] = df.Close.diff()
df["SMA_2"] = df.Close.rolling(2).mean()
df["Force_Index"] = df["Close"] * df["Volume"]
df["y"] = df["Diff"].apply(lambda x: 1 if x > 0 else 0).shift(-1)
df = df.drop(
   ["Open", "High", "Low", "Close", "Volume", "Diff", "Adj Close"],
   axis=1,
).dropna()
# print(df)
X = df.drop(["y"], axis=1).values
y = df["y"].values
X_train, X_test, y_train, y_test = train_test_split(
   X,
   y,
   test_size=0.2,
   shuffle=False,
)
clf = make_pipeline(StandardScaler(), MLPClassifier(random_state=0, shuffle=False))
clf.fit(
   X_train,
   y_train,
)

y_pred = clf.predict(X_test)
print(accuracy_score(y_test, y_pred))
print(y_pred[-1])
