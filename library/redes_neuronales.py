


def normaliza_pixeles(x_train, size, color=True):
    x_train_norm =  x_train.astype("float32") / 255.0
    if color:
        return x_train_norm.reshape(-1, size, size, 3)
    else:
        return x_train_norm.reshape(-1, size, size, 1)



def generator(x_train):

    datagen = ImageDataGenerator(
    featurewise_center=False,  # set input mean to 0 over the dataset
    samplewise_center=False,  # set each sample mean to 0
    featurewise_std_normalization=False,  # divide inputs by std of the dataset
    samplewise_std_normalization=False,  # divide each input by its std
    zca_whitening=False,  # apply ZCA whitening
    rotation_range = 30,  # randomly rotate images in the range (degrees, 0 to 180)
    zoom_range = 0.2, # Randomly zoom image 
    width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
    height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
    horizontal_flip = True,# randomly flip images
    fill_mode="nearest",
    shear_range=0.15,
    vertical_flip=False)  # randomly flip images

    datagen.fit(x_train)
    return datagen