from matplotlib import pyplot as plt
import pandas as pd

ticker = 'ETHUSDT'
ticker_df = pd.read_csv('./predictions/'+ticker+".csv", names=['y', 'y_pred'])

plt.plot(ticker_df[10:])
plt.show()gi