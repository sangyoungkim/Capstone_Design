import pandas as pd 
import matplotlib.pyplot as plt

main_data = pd.read_csv("datatest.csv")

print(main_data)
main_data.plot()
plt.title("speam HW")
plt.show()