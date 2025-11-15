from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# تعريف الرموز
HUMAN = 'O'
AI = 'X'
EMPTY = ' '


# دالة التحقق من الفائز
def check_winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # الصفوف
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # الأعمدة
        (0, 4, 8), (2, 4, 6)              # الأقطار
    ]
    for a, b, c in lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


# الخانات الفارغة
def available_moves(board):
    return [i for i, v in enumerate(board) if v == EMPTY]


# خوارزمية Minimax (مبسطة)
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == AI:
        return 1       # فوز الذكاء الاصطناعي
    if winner == HUMAN:
        return -1      # فوز اللاعب
    if not available_moves(board):
        return 0       # تعادل

    if is_maximizing:
        best_score = -10
        for m in available_moves(board):
            board[m] = AI
            score = minimax(board, False)
            board[m] = EMPTY
            if score > best_score:
                best_score = score
        return best_score
    else:
        best_score = 10
        for m in available_moves(board):
            board[m] = HUMAN
            score = minimax(board, True)
            board[m] = EMPTY
            if score < best_score:
                best_score = score
        return best_score


# اختيار أفضل حركة للذكاء الاصطناعي
def best_move(board):
    best_score = -10
    move_index = None
    for m in available_moves(board):
        board[m] = AI
        score = minimax(board, False)
        board[m] = EMPTY
        if score > best_score:
            best_score = score
            move_index = m
    return move_index


# صفحة الهبوط (Landing Page)
@app.route("/")
def landing():
    return render_template("landing.html")


# صفحة اللعبة
@app.route("/play")
def play():
    return render_template("index.html")


# صفحة معلومات المشروع
@app.route("/about")
def about():
    return render_template("about.html")


# API لحركة الذكاء الاصطناعي
@app.route("/ai-move", methods=["POST"])
def ai_move():
    data = request.get_json()
    board = data.get("board", [])
    move = best_move(board)
    return jsonify({"move": move})


if __name__ == "__main__":
    app.run(debug=True)
