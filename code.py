=== app.py ===
```python
from flask import Flask, render_template
import random

app = Flask(__name__)

# 2D array to represent the game board
game_board = [[" " for _ in range(3)] for _ in range(3)]

# Variable to keep track of the current player's symbol
current_player = "X"

# Function to check for a winner
def check_winner():
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] != " ":
            return game_board[i][0]
        if game_board[0][i] == game_board[1][i] == game_board[2][i] != " ":
            return game_board[0][i]
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != " ":
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != " ":
        return game_board[0][2]
    return None

# Function to check for a draw
def check_draw():
    for row in game_board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Function to reset the game board
def reset_game():
    global game_board
    game_board = [[" " for _ in range(3)] for _ in range(3)]

# Function to handle player input
def handle_input(row, col):
    global current_player
    if game_board[row][col] != " ":
        return False
    game_board[row][col] = current_player
    current_player = "O" if current_player == "X" else "X"
    return True

# Route for the game board display
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        row = int(request.form.get("row"))
        col = int(request.form.get("col"))
        if handle_input(row, col):
            winner = check_winner()
            if winner:
                return render_template("winner.html", symbol=winner)
            elif check_draw():
                return render_template("draw.html")
            return render_template("index.html", game_board=game_board)
    return render_template("index.html", game_board=game_board)

# Route for resetting the game
@app.route("/reset", methods=["POST"])
def reset():
    reset_game()
    return render_template("index.html", game_board=game_board)

if __name__ == "__main__":
    app.run(debug=True)
```

=== templates/index.html ===
```html
<!DOCTYPE html>
<html>
<head>
    <title>Tic Tac Toe</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>Tic Tac Toe</h1>
    <table>
        {% for row in game_board %}
        <tr>
            {% for cell in row %}
            <td>
                {% if cell == "X" %}
                <img src="{{ url_for('static', filename='x.png') }}" alt="X">
                {% elif cell == "O" %}
                <img src="{{ url_for('static', filename='o.png') }}" alt="O">
                {% else %}
                <form action="" method="POST">
                    <input type="hidden" name="row" value="{{ loop.parent.loop.index0 }}">
                    <input type="hidden" name="col" value="{{ loop.index0 }}">
                    <button type="submit">Click to place a symbol</button>
                </form>
                {% endif %}
            </td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    <form action="/reset" method="POST">
        <button type="submit">Reset Game</button>
    </form>
</body>
</html>
```

=== static/styles.css ===
```css
table {
    border-collapse: collapse;
}

td {
    width: 50px;
    height: 50px;
    border: 1px solid black;
    text-align: center;
    vertical-align: middle;
}

td img {
    width: 30px;
    height: 30px;
}
```

=== templates/winner.html ===
```html
<!DOCTYPE html>
<html>
<head>
    <title>Tic Tac Toe - Winner</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>Winner!</h1>
    <h2>{{ symbol }} wins!</h2>
    <form action="/" method="GET">
        <button type="submit">Play Again</button>
    </form>
</body>
</html>
```

=== templates/draw.html ===
```html
<!DOCTYPE html>
<html>
<head>
    <title>Tic Tac Toe - Draw</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>Draw!</h1>
    <h2>It's a draw! No one wins.</h2>
    <form action="/" method="GET">
        <button type="submit">Play Again</button>
    </form>
</body>
</html>
```

=== static/x.png ===
```png
image data for X
```

=== static/o.png ===
```png
image data for O
```

Note that this is just a basic implementation and you can improve it according to your needs. Also, you need to create the `x.png` and `o.png` images and place them in the `static` directory.