import pandas as pd
from sklearn.neural_network import MLPRegressor
import sys
import matplotlib.pyplot as plt
import pickle

csv_name = sys.argv[1]

mat_data = pd.read_csv(csv_name, delimiter=';')  # read rows
mat_data = mat_data.sample(n=len(mat_data), random_state=43) # shuffle rows
mat_inputs = mat_data

x_mat = mat_data.drop(columns='G3')
y_mat = mat_data['G3']
mat_count = mat_data.shape[0]
mat_train_size = int(mat_count * 0.7)
mat_val_size = int(mat_count * 0.2)

x_mat_train_and_val = x_mat[:(mat_train_size + mat_val_size)]
y_mat_train_and_val = y_mat[:(mat_train_size + mat_val_size)]
x_mat_train = x_mat[:mat_train_size]
y_mat_train = y_mat[:mat_train_size]
x_mat_val = x_mat_train_and_val[mat_train_size:]
y_mat_val = y_mat_train_and_val[mat_train_size:]
x_mat_test = x_mat[(mat_train_size + mat_val_size):]
y_mat_test = y_mat[(mat_train_size + mat_val_size):]

mlp = MLPRegressor(solver='adam', hidden_layer_sizes=(50, 50), max_iter=3000,
                   early_stopping=False, beta_1=0.9, learning_rate_init=0.0001,
                   random_state=0, validation_fraction=0,
                   verbose=True, activation='identity', alpha=0.001)
mlp.fit(x_mat_train, y_mat_train)

# Loss function visualisation
pd.DataFrame(mlp.loss_curve_).plot()

print('R2 score for TRAIN: ' + str(mlp.score(x_mat_train, y_mat_train)))
print('R2 score for VAL: ' + str(mlp.score(x_mat_val, y_mat_val)))
print('R2 score for TEST: ' + str(mlp.score(x_mat_test, y_mat_test)))

y_predicted_train = mlp.predict(x_mat_train)
y_predicted_val = mlp.predict(x_mat_val)
y_predicted_test = mlp.predict(x_mat_test)

train_count = x_mat_train.shape[0]
train_accurate_count = 0
val_count = x_mat_val.shape[0]
val_accurate_count = 0
test_count = x_mat_test.shape[0]
test_accurate_count = 0

# 1 for SPLIT1, 0.05 for SPLIT2
threshold = 1.0

for i in range(x_mat_train.shape[0]):
    if abs(y_mat_train.iloc[i] - y_predicted_train[i]) < threshold:
        train_accurate_count = train_accurate_count + 1
for i in range(x_mat_val.shape[0]):
    if abs(y_mat_val.iloc[i] - y_predicted_val[i]) < threshold:
        val_accurate_count = val_accurate_count + 1
for i in range(x_mat_test.shape[0]):
    if abs(y_mat_test.iloc[i] - y_predicted_test[i]) < threshold:
        test_accurate_count = test_accurate_count + 1

print('TRAIN accuracy = ' + str(train_accurate_count / train_count * 100) + '% (' + str(train_accurate_count) + '/' + str(train_count) + ')')
print('VAL accuracy = ' + str(val_accurate_count / val_count * 100) + '% (' + str(val_accurate_count) + '/' + str(val_count) + ')')
print('TEST accuracy = ' + str(test_accurate_count / test_count * 100) + '% (' + str(test_accurate_count) + '/' + str(test_count) + ')')

# Test results visualisation
fig = plt.figure()
plt.title('Real vs predicted')
plt.xlabel('Students')
plt.ylabel('Scores')
ax1 = fig.add_subplot(111)
ax1.scatter(range(x_mat_val.shape[0]), y_mat_val, s=10, c='b', marker="s", label='real')
ax1.scatter(range(x_mat_val.shape[0]), y_predicted_val, s=10, c='r', marker="o", label='predicted')
ax1.legend()

plt.show()

filename = 'model_split1_mat.sav'
pickle.dump(mlp, open(filename, 'wb'))
