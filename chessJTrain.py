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
import tensorflow as tf
import os

train_boards, train_moves, test_boards, test_moves = get_train_data(
    20000, 5000)

model = create_model()
# model.load_weights("model/cp.ckpt")

print('Training...')

checkpoint_path = "model/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

model.fit(train_boards, train_moves, epochs=20, validation_data=(
    test_boards, test_moves), callbacks=[cp_callback])

print('Evaluating...')

test_loss, test_acc = model.evaluate(test_boards, test_moves, verbose=2)

print('Accuracy:', test_acc)
