# ChessJ readme

## Help to train the model

To help train the model, clone this repo locally.

You also need the training data. Download it from this link: [https://gomarus-my.sharepoint.com/:u:/g/personal/142584_gomarus_nl/ETd04e0FjqRLhoPR0D1dUy4BGwkZsJlykmbGeBNXI3uhHg?e=9vWqU3](https://gomarus-my.sharepoint.com/:u:/g/personal/142584_gomarus_nl/ETd04e0FjqRLhoPR0D1dUy4BGwkZsJlykmbGeBNXI3uhHg?e=9vWqU3)

Then install tensorflow.

If you want to, change line 26 in `chessJTrain.py` from:

```python
model = create_model()
```

to

```python
model = create_model(True)
```

to train the advanced version of the model. (Very much appreciated)

Then run `python chessJTrain.py` to train the model.

After that, move the files `cp.ckpt.data-00000-of-00001` and `cp.ckpt.index` from `./model` to `./model/[simple|advanced]/[Your name]-[Version]`.
Then create a pull request to return the trained model.
