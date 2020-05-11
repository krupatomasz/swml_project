import pandas as pd
from sklearn.neural_network import MLPRegressor
import sys
import matplotlib.pyplot as plt

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

mlp = MLPRegressor(solver='adam', hidden_layer_sizes=50, max_iter=1000,
                   random_state=1, validation_fraction=2/9, verbose=True)
mlp.fit(x_mat_train, y_mat_train)

# Loss function visualisation
pd.DataFrame(mlp.loss_curve_).plot()

print('R2 score: ' + str(mlp.score(x_mat_test, y_mat_test)))
y_predicted = mlp.predict(x_mat_test)

count = x_mat_test.shape[0]
accurate_count = 0

for i in range(x_mat_test.shape[0]):
    if abs(y_mat_test.iloc[i] - y_predicted[i]) < 0.05:
        accurate_count = accurate_count + 1

print('Accuracy = ' + str(accurate_count / count * 100) + '% (' + str(accurate_count) + '/' + str(count) + ')')

# Test results visualisation
fig = plt.figure()
plt.title('Real vs predicted')
plt.xlabel('Students')
plt.ylabel('Scores')
ax1 = fig.add_subplot(111)
ax1.scatter(range(x_mat_test.shape[0]), y_mat_test, s=10, c='b', marker="s", label='real')
ax1.scatter(range(x_mat_test.shape[0]), y_predicted, s=10, c='r', marker="o", label='predicted')
ax1.legend()

plt.show()

