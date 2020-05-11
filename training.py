import pandas as pd
from sklearn.neural_network import MLPRegressor
import sys

csv_name = sys.argv[1]

mat_data = pd.read_csv(csv_name, delimiter=';').sample(frac=1)  # read and shuffle rows
mat_inputs = mat_data

x_mat = mat_data.drop(columns='G3')
y_mat = mat_data['G3']
mat_count = mat_data.shape[0]
mat_train_size = int(mat_count * 0.9)

x_mat_train = x_mat[:mat_train_size]
y_mat_train = y_mat[:mat_train_size]
x_mat_test = x_mat[mat_train_size:]
y_mat_test = y_mat[mat_train_size:]

mlp = MLPRegressor(solver='lbfgs', hidden_layer_sizes=50, max_iter=500,
                   random_state=1, validation_fraction=2/9, verbose=True)
mlp.fit(x_mat_train, y_mat_train)
print(mlp.score(x_mat_test, y_mat_test))
print("Done234")
