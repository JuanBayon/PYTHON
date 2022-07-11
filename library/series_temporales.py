import numpy as np
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import RMSprop
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN


"""
RED NEURONAL RECURSIVA EN SERIES TEMPORALES

1. Analizamos los datos y vemos si se repiten comportamientos a lo largo del tiempo.
2. Definimos el tipo de entrenamiento que vamos a utilizar:
    2.1. Si los datos se repiten a lo largo del tiempo (estacionalidad) --> entrenamos el modelo dándole como dato de entrenamiento una parte bien representativa de todo el conjunto de datos
    2.2. Si los datos no se repiten a lo largo del tiempo --> tenemos que entrenar dándole poco a poco todo el conjunto de datos. 
3. Repetimos los 'step' últimos valores del conjunto de entrenamiento y de test. 
4. Redimensionamos los datos de entrenamiento y de test para que tengan la forma de (NºBatches, 1, step). 'step'=='embedding'.
5. Entrenamos el modelo utilizando RNN, SimpleRNN, LSTM, etc
6. Dependiendo del resultado probamos diferentes arquitecturas, tamaño de ventana (step), batch_size, épocas, (...)
7. Nos quedamos con el mejor modelo.

"""


def convertToMatrix(data, step):
    """
    Convierte los datos en grupos de datos iguales al step
    para calcular el modelo de una serie temporal.
    """
    np.append(data, np.repeat(data[-1,], step))
    X, Y =[], []
    for i in range(len(data)-step):
        d=i+step  
        X.append(data[i:d,])
        Y.append(data[d,])
    return np.array(X), np.array(Y)


def reshape(trainX, testX):
    trainX2 = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX2 = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    return trainX2, testX2




def build_simple_lstn(num_units=128, embedding=4, num_dense=32,lr=0.001):
    """
    Builds and compiles a simple RNN model
    Arguments:
            num_units: Number of units of a the simple RNN layer
            embedding: Embedding length
            num_dense: Number of neurons in the dense layer followed by the RNN layer
            lr: Learning rate (uses RMSprop optimizer)
    Returns:
            A compiled Keras model.
    """
    model = Sequential()
    # Long short term memory
    model.add(LSTM(units=num_units, input_shape=(1,embedding), activation="relu"))
    model.add(Dense(num_dense, activation="relu"))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=RMSprop(lr=lr),metrics=['mse'])
    
    return model



def build_simple_rnn(num_units=128, embedding=4,num_dense=32,lr=0.001):
    """
    Builds and compiles a simple RNN model
    Arguments:
            num_units: Number of units of a the simple RNN layer
            embedding: Embedding length
            num_dense: Number of neurons in the dense layer followed by the RNN layer
            lr: Learning rate (uses RMSprop optimizer)
    Returns:
            A compiled Keras model.
    """
    model = Sequential()
    model.add(SimpleRNN(units=num_units, input_shape=(1,embedding), activation="relu"))
    model.add(Dense(num_dense, activation="relu"))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=RMSprop(lr=lr),metrics=['mse'])
    
    return model



def predictions(model,trainX,testX):
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    predicted = np.concatenate((trainPredict,testPredict),axis=0)
    
    return predicted



def plot_compare(df, predicted, Tp):
    """
    # Total time points
    N = 3000
    # Time point to partition train/test splits
    Tp = 750   
    """
    index = df.index.values
    plt.figure(figsize=(15,4))
    plt.title("Ground truth and prediction together",fontsize=18)
    plt.plot(index,df,c='blue')
    plt.plot(index,predicted,c='orange',alpha=0.75)
    plt.legend(['True data','Predicted'],fontsize=15)
    plt.axvline(df.index[Tp], c="r")
    plt.grid(True)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()



def prepare_data(df, Tp, N, step=4):
    """
    # Total time points
    N = 3000
    # Time point to partition train/test splits
    Tp = 750   
    """
    values = df.values
    train, test = values[0:Tp,:], values[Tp:N,:]
    test = np.append(test,np.repeat(test[-1,],step))
    train = np.append(train,np.repeat(train[-1,],step))
    trainX, trainY =convertToMatrix(train,step)
    testX, testY =convertToMatrix(test,step)
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    
    return trainX,testX,trainY,testY



def errors(testX, df, Tp, N):
    """
    # Total time points
    N = 3000
    # Time point to partition train/test splits
    Tp = 750   
    """
    y_true = df[Tp:N].values
    y_pred = model.predict(testX)
    error = y_pred - y_true
    return [mean_absolute_error(y_true=y_true, y_pred=y_pred)]



# EMBEDING/ STEP
for s in [2,4,6,8,10,12]:
    trainX,testX,trainY,testY = prepare_data(s)
    model = build_simple_rnn(num_units=32,num_dense=8,embedding=s)
    batch_size=16
    num_epochs = 100
    model.fit(trainX,trainY, 
        epochs=num_epochs, 
        batch_size=batch_size,
        verbose=0)
    preds = predictions(model,trainX,testX)
    print("Embedding size: {}".format(s))
    print("Error:", errors(testX, df))
    print("-"*100)
    plot_compare(preds)
    print()



# EPOCHS
for e in [100,200,300,400,500]:
    trainX, testX, trainY, testY = prepare_data(8)
    model = build_simple_rnn(num_units=32,num_dense=8,embedding=8)
    batch_size=16
    num_epochs = e
    model.fit(trainX,trainY, 
        epochs=num_epochs, 
        batch_size=batch_size,
        verbose=0)
    preds = predictions(model,trainX,testX)
    print("Ran for {} epochs".format(e))
    print("Error:", errors(testX, df))
    print("-"*100)
    plot_compare(preds)
    print()



#BATCH SIZE 
for b in [4,8,16,32,64]:
    trainX,testX,trainY,testY = prepare_data(8)
    model = build_simple_rnn(num_units=32,num_dense=8,embedding=8)
    batch_size=b
    num_epochs = 250
    model.fit(trainX,trainY, 
        epochs=num_epochs, 
        batch_size=batch_size,
        verbose=0)
    preds = predictions(model,trainX,testX)
    print("Ran with batch size: {}".format(b))
    print("Error:", errors(testX, df))
    print("-"*100)
    plot_compare(preds)
    print()


def separa_datos_way2(values, iteraciones=4):

    train = []
    test = []
    train_index = []
    test_index = []

    particion = iteraciones / 2
    iteracion = round(N/particion)
    resto = N - iteracion
    tst = round(resto / (iteraciones - 1))
    tr = iteracion - tst

    for i in range(iteraciones):
        train_index.append(tr)
        test_index.append(tst)
        train_values, test_values = values[0:tr, :], values[tr:iteracion, :]
        train.append(train_values)
        test.append(test_values)
        tr = iteracion
        iteracion += tst

    return train, test, train_index, test_index


def entrena_linea_temporal_way2(df, N, batch_size=16, num_epochs=100, step=4, iteraciones=4):

        values = df.values
        resultado = separa_datos_way2(values, iteraciones)
        train = resultado[0]
        test = resultado[1]
        train_index = resultado[2]
        test_index = resultado[3]
        histories = []

        for i, (semitrain, semitest, semitest_index, semitrain_index) in enumerate(zip(train, test, test_index, train_index)):
                test = np.append(semitest, np.repeat(semitest[-1,], step))
                train = np.append(semitrain, np.repeat(semitrain[-1,], step))
                trainX, trainY = convertToMatrix(semitrain, step)
                testX, testY = convertToMatrix(semitest, step)
                trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
                testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
                print(trainX.shape)
                print(testX.shape)
                if i == 0:
                        model = build_simple_lstn()
                        model.summary()
                history = model.fit(trainX,trainY, 
                                epochs=num_epochs, 
                                batch_size=batch_size,
                                verbose=1)
                model.save("my_model.h5")
                histories.append(history)

                # acc = history.history['accuracy']
                # val_acc = history.history['val_accuracy']
                # loss = history.history['loss']
                # val_loss = history.history['val_loss']

                
                # trainPredict = model.predict(trainX)
                # testPredict = model.predict(testX)

                # total = semitrain_index + semitest_index
                # predicted = np.concatenate((trainPredict,testPredict),axis=0)

                # plt.figure(figsize=(15,4))
                # plt.title("Ground truth and prediction together",fontsize=18)
                # plt.plot(df.iloc[range(total)],c='blue')
                # plt.plot(predicted,c='orange',alpha=0.75)
                # plt.legend(['True data','Predicted'],fontsize=15)
                # plt.axvline(df.index[semitest_index], c="r")
                # plt.grid(True)
                # plt.xticks(fontsize=14)
                # plt.yticks(fontsize=14)
                # plt.show()

                # error = predicted[semitest_index:N]-df[semitest_index:N]
                # error = np.array(error).ravel()
                # plt.figure(figsize=(7,5))
                # plt.hist(error,bins=25,edgecolor='k',color='orange')
                # plt.show()

        return model, history