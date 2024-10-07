import numpy as np
import pandas as pd

data = np.random.random(size=(100, 20))
df = pd.DataFrame(data=data)

print(df.to_string())
