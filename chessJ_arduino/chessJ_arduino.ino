#define RANGE(var, i) \
    int var = 0;      \
    var < i;          \
    var++

const int boardHeight = 8;
const int boardWidth = 8;

const int boardPins[boardHeight][boardWidth] = {
    {20, 6, 10, 22, 26, 30, 34, 38},
    {18, 7, 11, 23, 27, 31, 35, 39},
    {4, 8, 12, 24, 28, 32, 36, 40},
    {5, 9, 21, 25, 29, 33, 37, 41},
    {17, A15, A11, A7, A3, 53, 49, 45},
    {16, A14, A10, A6, 13, 52, 48, 44},
    {15, A13, A9, A5, A1, 51, 47, 43},
    {14, A12, A8, A4, A0, 50, 46, 42},
};

bool boardState[boardHeight][boardWidth] = {};
bool changed = false;

void setup()
{
    Serial.begin(9600);
    for (RANGE(y, boardHeight))
    {
        for (RANGE(x, boardWidth))
        {
            pinMode(boardPins[y][x], INPUT);
            boardState[y][x] = digitalRead(boardPins[y][x]);
        }
    }
}

void loop()
{
    for (RANGE(y, boardHeight))
    {
        for (RANGE(x, boardWidth))
        {
            bool value = digitalRead(boardPins[y][x]);
            if (value != boardState[y][x])
            {
                changed = true;
                Serial.print(y);
                Serial.print(' ');
                Serial.print(x);
                Serial.print(' ');
                Serial.println(int(value));
            }
            boardState[y][x] = value;
        }
    }
    changed = false;
}
