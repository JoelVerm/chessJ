#define RANGE(var, i) \
    int var = 0;      \
    var < i;          \
    var++

const int boardHeight = 8;
const int boardWidth = 8;

const int boardPins[boardHeight][boardWidth] = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
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
                Serial.println(value);
            }
            boardState[y][x] = value;
        }
    }
    changed = false;
}
