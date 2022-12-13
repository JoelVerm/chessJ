print("""


       ............************
       ............************
       ............************           ******,     **     **    **********    *******     *******       .......
       ............************         ***     **    **     **    **           **     **   **     **           ..
       ............************         **.           **     **    **           **          **                  ..
      ************............          **.           *********    *********     *******     *******            ..
      ************............          **.           **     **    **                  **          **           ..
      ************............           **    ***    **     **    **           **     **   **     **   ...    ...
      ************............            ******      **     **    **********    *******     *******      ......
      ************


""")

from chessJGetData import get_train_data
from chessJModel import create_model
from chessJUtil import input_int, select_folder
import tensorflow as tf
import os

train_set_size = input_int('choose the train set size (~5000-200000): ')
test_set_size = input_int('choose the test set size (~2000-50000): ')

train_boards, train_moves, test_boards, test_moves = get_train_data(
    train_set_size, test_set_size)

create_advanced = input_int('choose the level of the model to train (0-1): ')
model = create_model(create_advanced == 1)
if input('do you want to load an existing model? (y/n): ') == 'y':
    model_load_folder = select_folder('model')
    model.load_weights(f'{model_load_folder}/cp.ckpt')

print('Select a folder to save the model to')

model_save_folder = select_folder('model')
checkpoint_path = f'{model_save_folder}/cp.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)

print('Training...')

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

model.fit(train_boards, train_moves, epochs=20, validation_data=(
    test_boards, test_moves), callbacks=[cp_callback])

print('Evaluating...')

test_loss, test_acc = model.evaluate(test_boards, test_moves, verbose=2)

print('Accuracy:', test_acc)
