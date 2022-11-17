# ChessJ readme

## Play against the AI

To play against the AI, just run `chessJ.py` and follow the instructions in the terminal.

The algorithm at the moment is incapable of recognizing check or checkmate. You have to look for that yourselves. Just type `q` for `quit` or `x` for `exit` to stop the game.

## Help to train the model

To help train the model, clone this repo locally.

You also need the training data. Download it from this link: [https://gomarus-my.sharepoint.com/:u:/g/personal/142584_gomarus_nl/ETd04e0FjqRLhoPR0D1dUy4BGwkZsJlykmbGeBNXI3uhHg?e=9vWqU3](https://gomarus-my.sharepoint.com/:u:/g/personal/142584_gomarus_nl/ETd04e0FjqRLhoPR0D1dUy4BGwkZsJlykmbGeBNXI3uhHg?e=9vWqU3)

Then install tensorflow.

<br>

If you want to, change line 26 in `chessJTrain.py` from:

```python
model = create_model()
```

to

```python
model = create_model(True)
```

to train the advanced version of the model. (Very much appreciated 😉)

<br>

In the same file on the next line, a commented-out function `model.load_weights` can be uncommented to load the previous version of the model before training.

(I forgot to comment it out last time 😏)

<br>

You can also change the dataset size by modifying line 23 in `chessJTrain.py`:

```python
train_boards, train_moves, test_boards, test_moves = get_train_data(
    20000, 5000)
```

20000 is the train set size, 5000 the test set size.

<br>

Then run `python chessJTrain.py` to train the model.

You will see accuracy does not reach high values. That is not a big problem and is due to the nature of chess. There are so many possible boards that the model does not get very good on a per-situation basis. However, measured over a whole game it probably will be good enough.

<br>

After that, move the files `cp.ckpt.data-00000-of-00001` and `cp.ckpt.index` from `./model` to `./model/[simple|advanced]/[Your name]-[Version]`.
Then create a pull request to return the trained model.
