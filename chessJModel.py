import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf


def create_model(advanced=False):
    print('Creating model...')

    if advanced:
        input = tf.keras.Input(shape=(8, 8, 13))
        f0 = tf.keras.layers.Flatten()(input)
        # step 1
        para_relu_1 = tf.keras.layers.PReLU()
        d11 = tf.keras.layers.Dense(64, activation=para_relu_1)(f0)
        c1 = tf.keras.layers.Conv2D(64, 3, activation='relu')(input)
        f1 = tf.keras.layers.Flatten()(c1)
        d12 = tf.keras.layers.Dense(64, activation=para_relu_1)(f1)
        a1 = tf.keras.layers.Add()([d11, d12])
        # step 2
        para_relu_2 = tf.keras.layers.PReLU()
        d21 = tf.keras.layers.Dense(8**3, activation=para_relu_2)(a1)
        c2 = tf.keras.layers.Conv2D(8**3, 3, activation='relu')(c1)
        f2 = tf.keras.layers.Flatten()(c2)
        d22 = tf.keras.layers.Dense(8**3, activation=para_relu_2)(f2)
        a2 = tf.keras.layers.Add()([d21, d22])
        # step 3
        para_relu_3 = tf.keras.layers.PReLU()
        d31 = tf.keras.layers.Dense(8**4, activation=para_relu_3)(a2)
        c3 = tf.keras.layers.Conv2D(8**4, 3, activation='relu')(c2)
        f3 = tf.keras.layers.Flatten()(c3)
        d32 = tf.keras.layers.Dense(8**4, activation=para_relu_3)(f3)
        a3 = tf.keras.layers.Add()([d31, d32])
        # end
        output = tf.keras.layers.Dense(8**4, activation=para_relu_3)(a3)
        model = tf.keras.Model(inputs=input, outputs=output)
    else:
        model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(8, 8, 13)),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(8**3, activation="relu"),
            tf.keras.layers.Dense(8**4, activation="relu")
        ])

    print('Compiling...')

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(
                      from_logits=True),
                  metrics=['accuracy'])

    return model
