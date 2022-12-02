# ChessJ readme

## Play against the AI

To play against the AI, just run `chessJ.py` and follow the instructions in the terminal.

At the moment, the algorithm is incapable of recognizing check or checkmate. You have to look for that yourselves. Just type `q` for `quit` or `x` for `exit` to stop the game.

## Help to train the model

To help train the model, clone this repo locally.

You also need the training data. Download it from this link: [https://gomarus-my.sharepoint.com/:u:/g/personal/142584_gomarus_nl/ETd04e0FjqRLhoPR0D1dUy4BGwkZsJlykmbGeBNXI3uhHg?e=9vWqU3](https://gomarus-my.sharepoint.com/:u:/g/personal/142584_gomarus_nl/ETd04e0FjqRLhoPR0D1dUy4BGwkZsJlykmbGeBNXI3uhHg?e=9vWqU3)

Then install tensorflow.

Make sure to create a new folder to save your trained model at this path: `./model/cache/[simple|advanced]/[your name]-[version]`

Run `python chessJTrain.py` to train the model.

Follow the instructions in the terminal to set the dataset sizes, version of the model and save location.

You will see accuracy does not reach high values. That is not a big problem and is due to the nature of chess. There are so many possible boards that the model does not get very good on a per-situation basis. However, measured over a whole game it probably will be good enough.
s
After training, the files will be in your specified folder. Create a pull request to return the trained model.
