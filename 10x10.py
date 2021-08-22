from math import inf as infinity
from random import choice
import platform
import time
from os import system


HUMAN = -1
COMP = +1

# Trạng thái ban đầu của bảng (ma trận 3x3) khi chưa chơi
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def evaluate(state):
    """
    Hàm lượng giá trạng thái hiejn tại
    Tham số state : trạng thái hiện tại của bảng
    :return: Máy thắng thì trả về +1, Người thắng thì trả về -1, hòa thì trả về 0
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    Hàm kiểm tra xem nếu máy hoặc người thắng. Các khả năng xảy ra :
    * Các hàng ngang   [X X X X X] or [O O O O O]
    * Các cột dọc      [X X X X X] or [O O O O O]
    * Các đường chéo  [X X X X X] or [O O O O O]
    :param state : trạng thái hiện tại của bảng
    :param player : nhận giá trị là HUMAN (người chơi) hoặc COMP (máy tính)
    :return: Trả về True nếu player thắng, ngược lại trả về False
    """
    # Ma trận này chứa các khả năng chiến thắng của player
    win_state = []
    # Các hàng ngang và cột dọc
    for i in range(10):
        for j in range(6):
            win_state.append([state[i][j], state[i][j+1], state[i][j+2], state[i][j+3], state[i][j+4]])
            win_state.append([state[j][i], state[j+1][i], state[j+2][i], state[j+3][i], state[j+4][i]])

    # Các đường chéo

    # hai đường chéo chính
    for i in range(6):
        win_state.append([state[9-i][i], state[9-i-1][i+1], state[9-i-2][i+2], state[9-i-3][i+3], state[9-i-4][i+4]])
        win_state.append([state[i][i], state[i+1][i+1], state[i+2][i+2], state[i+3][i+3], state[i+4][i+4]])

    # 4 đường chéo xung quanh 2 đường chéo chính
    for i in range(1,6):
        win_state.append([state[10-i][i], state[10-i-1][i+1], state[10-i- 2][i+2], state[10-i-3][i+3], state[10-i-4][i+4]])
        win_state.append([state[9-i][i-1], state[9-i-1][i], state[9-i-2][i+1], state[9-i-3][i+2], state[9-i-4][i+3]])
        win_state.append([state[i][i-1], state[i+1][i], state[i+2][i+1], state[i+3][i+2], state[i+4][i+3]])
        win_state.append([state[i-1][i], state[i][i+1], state[i+1][i+2], state[i+2][i+3], state[i+3][i+4]])

    # các đường chéo còn lại
    for i in range(1, 5):
        win_state.append([state[9-i+1][i+1], state[9-i][i+2], state[9-i-1][i+3], state[9-i-2][i+4], state[9-i-3][i+5]])
        win_state.append([state[7-i+1][i-1], state[7-i][i], state[7-i-1][i+1], state[7-i-2][i+2], state[7-i-3][i+3]])
        win_state.append([state[i+1][i-1], state[i+2][i], state[i+3][i+1], state[i+4][i+2], state[i+5][i+3]])
        win_state.append([state[i-1][i+1], state[i][i+2], state[i+1][i+3], state[i+2][i+4], state[i+3][i+5]])

    for i in range(1, 4):
        win_state.append([state[9-i+1][i+2], state[9-i][i+3], state[9-i-1][i+4], state[9-i-2][i+5], state[9-i-3][i+6]])
        win_state.append([state[7-i][i-1], state[7-i-1][i], state[7-i-2][i+1], state[7-i-3][i+2], state[7-i-4][i+3]])
        win_state.append([state[i+2][i-1], state[i+3][i], state[i+4][i+1], state[i+5][i+2], state[i+6][i+3]])
        win_state.append([state[i-1][i+2], state[i][i+3], state[i+1][i+4], state[i+2][i+5], state[i+3][i+6]])

    for i in range(1, 3):
        win_state.append([state[9-i+1][i+3], state[9-i][i+4], state[9-i-1][i+5], state[9-i-2][i+6], state[9-i-3][i+7]])
        win_state.append([state[7-i-1][i-1], state[7-i-2][i], state[7-i-3][i+1], state[7-i-4][i+2], state[7-i-5][i+3]])
        win_state.append([state[i+3][i-1], state[i+4][i], state[i+5][i+1], state[i+6][i+2], state[i+7][i+3]])
        win_state.append([state[i-1][i+3], state[i][i+4], state[i+1][i+5], state[i+2][i+6], state[i+3][i+7]])


    win_state.append([state[9][5], state[8][6], state[7][7], state[6][8], state[5][9]])
    win_state.append([state[4][0], state[3][1], state[2][2], state[1][3], state[0][4]])
    win_state.append([state[0][5], state[1][6], state[2][7], state[3][8], state[4][9]])
    win_state.append([state[5][0], state[6][1], state[7][2], state[8][3], state[9][4]])

    if [player, player, player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    Hàm này kiểm tra xem nếu máy tính hoặc người chơi thắng
    :param state : trạng thái hiện tại của bảng
    :return: Trả về True nếu 1 trong 2 HUMAN (người chơi) hoặc COMP (máy tính) thắng, ngược lại trả về False
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Mỗi ô trống trong bảng chưa được máy tính hoặc người điền thì sẽ được thêm vào list cells dưới dạng tọa đọo
        [hàng trống, cột trống]
    :param state : trạng thái hiện tại của bảng
    :return: danh sách các ô trống trong ma trận chưa được HUMAN hoặc COMP điền
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    Hàm này kiểm tra xem bước đi có hợp lệ hay không (hợp lệ tứ là đi vào ô trống trong bảng hiện tại), thường là để
            kiểm tra xem người chơi HUMAN có chọn ô hợp lệ không
    :param x: tọa độ x (tức là hàng ngang) của bảng
    :param y: tọa độ y (tức là cột) của bảng
    :return: Trả về True nếu ô board[x][y] trống, ngược lại trả về False
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Tiến hành lượt đi của player lên bảng hiện tại nếu như tọa độ [x, y] hợp lệ
    :param x: tọa độ x (tức là hàng ngang) của bảng
    :param y: tọa độ y (tức là cột) của bảng
    :param player: người chơi hiện tại
    :return : Trả về True nếu lượt đi hợp lệ đã được tiến hành, ngược lại trả về False
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    Hàm AI chọn nước đi tốt nhất cho COMP (máy tính)
    :param state : trạng thái hiện tại của bảng
    :param depth: các đốt trên cây trò chơi hiện tại, tức là các ô còn trống (0 <= depth <= 9),
        nhưng trong hàm này thì không nhận 9 (xem hàm ai_turn(), nếu máy được đi trước tức depth = 9 thì máy
        sẽ chọn ngẫu nhiên 1 trong 9 ô, khi depth <=8 thì hàm này mới được gọi để chọn nước đi tối ưu)
    :param player : nhận giá trị là HUMAN (người chơi) hoặc COMP (máy tính)
    :return: một list với [hàm tối ưu, cột tối ưu, điểm số tối ưu]
    """

    # Máy tính và người chơi sẽ bắt đầu với điểm số thấp nhất
    # Nếu là máy tính (+1) sẽ bắt đầu với điểm số - vô cùng
    # Nếu là con người (-1) sẽ bắt đầu với điểm số + vô cùng
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    # Kiểm tra xem đã tới trạng thái kết thúc của đốt trong cây trò chơi chưa
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    """
    Vòng lặp này sẽ duyệt qua các trường hợp máy có thể đi
    Trong vòng lặp có chứa đệ quy minimax(state, depth - 1, -player) sẽ duyệt các nước đi có thể của đối thủ rồi tới 
        nước đi của máy, thay phiên, và tiếp tục lặp lại, khi tới trạng thái kết thúc, đệ quy sẽ quay lui lại, nếu là 
        lượt đi của người chơi thì sẽ chọn nước đi có điểm số thấp nhất, nếu là lượt của máy thì sẽ chọn nước đi có 
        điểm số cao nhất, và cuối cùng là trả về nước đi tối ưu cho máy
    Hàm này sẽ tối ưu nếu đối thủ chơi tối ưu
    """

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    Xóa màn hình console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    In bảng hiện tại lên màn hình console
    :param state: trạng thái của bảng hiện tại
    :param c_choice : máy chọn O hoặc X
    :param h_choice : người chọn O hoặc X
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '--------------------------------------------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    Gọi hàm minimax nếu depth < 9, ngược lại thì chọn một tọa độ ngẫu nhiên trong bảng
    :param c_choice: máy chọn X or O
    :param h_choice: người chọn X or O
    :return:
    """

    # Ngưng nếu trò chơi kết thúc
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Xóa màn hình console cũ
    clean()

    # In màn hình console hiện tại
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    # Chọn nước đi tối ưu của máy
    if depth == 9:
        x = choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    Chọn nước đi hợp lệ của người chơi (HUMAN)
    :param c_choice: máy chọn X or O
    :param h_choice: người chọn X or O
    :return:
    """

    # Ngưng nếu trò chơi kết thúc
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dict chứa các nước đi mà người có thể chọn
    move = -1
    moves = {
    1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [0, 4], 6: [0, 5], 7: [0, 6], 8: [0, 7], 9: [0, 8], 10: [0, 9],
    11: [1, 0], 12: [1, 1], 13: [1, 2], 14: [1, 3], 15: [1, 4], 16: [1, 5], 17: [1, 6], 18: [1, 7], 19: [1, 8], 20: [1, 9],
    21: [2, 0], 22: [2, 1], 23: [2, 2], 24: [2, 3], 25: [2, 4], 26: [2, 5], 27: [2, 6], 28: [2, 7], 29: [2, 8], 30: [2, 9],
    31: [3, 0], 32: [3, 1], 33: [3, 2], 34: [3, 3], 35: [3, 4], 36: [3, 5], 37: [3, 6], 38: [3, 7], 39: [3, 8], 40: [3, 9],
    41: [4, 0], 42: [4, 1], 43: [4, 2], 44: [4, 3], 45: [4, 4], 46: [4, 5], 47: [4, 6], 48: [4, 7], 49: [4, 8], 50: [4, 9],
    51: [5, 0], 52: [5, 1], 53: [5, 2], 54: [5, 3], 55: [5, 4], 56: [5, 5], 57: [5, 6], 58: [5, 7], 59: [5, 8], 60: [5, 9],
    61: [6, 0], 62: [6, 1], 63: [6, 2], 64: [6, 3], 65: [6, 4], 66: [6, 5], 67: [6, 6], 68: [6, 7], 69: [6, 8], 70: [6, 9],
    71: [7, 0], 72: [7, 1], 73: [7, 2], 74: [7, 3], 75: [7, 4], 76: [7, 5], 77: [7, 6], 78: [7, 7], 79: [7, 8], 80: [7, 9],
    81: [8, 0], 82: [8, 1], 83: [8, 2], 84: [8, 3], 85: [8, 4], 86: [8, 5], 87: [8, 6], 88: [8, 7], 89: [8, 8], 90: [8, 9],
    91: [9, 0], 92: [9, 1], 93: [9, 2], 94: [9, 3], 95: [9, 4], 96: [9, 5], 97: [9, 6], 98: [9, 7], 99: [9, 8], 100: [9, 9]
    }

    # Xóa mà hình console cũ
    clean()

    # In màn hình console hiện tại
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    # Người chơi nhập nước đi của mình, nếu nước đi không hợp lệ, in ra "Bad choice" và yêu cầu nhập lại
    while move < 1 or move > 100:
        try:
            move = int(input('Use numpad (1..100): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

def set_FT(state, c_choice, h_choice):
    """
    Hàm này đặt trạng thái đầu tiên cho game, nhập số lượt đi trước của máy, chọn các vị trí mà máy đi xong nhập
        số lượt đi trước của người rồi các vị trí mà người đi
    :param state: trạng thái hiện tại
    :param c_choice: máy chọn X hoặc O
    :param h_choice: người chọn X hoặc O
    :return: số lượt đi trước của máy và người
    """

    moves = {
    1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [0, 4], 6: [0, 5], 7: [0, 6], 8: [0, 7], 9: [0, 8], 10: [0, 9],
    11: [1, 0], 12: [1, 1], 13: [1, 2], 14: [1, 3], 15: [1, 4], 16: [1, 5], 17: [1, 6], 18: [1, 7], 19: [1, 8], 20: [1, 9],
    21: [2, 0], 22: [2, 1], 23: [2, 2], 24: [2, 3], 25: [2, 4], 26: [2, 5], 27: [2, 6], 28: [2, 7], 29: [2, 8], 30: [2, 9],
    31: [3, 0], 32: [3, 1], 33: [3, 2], 34: [3, 3], 35: [3, 4], 36: [3, 5], 37: [3, 6], 38: [3, 7], 39: [3, 8], 40: [3, 9],
    41: [4, 0], 42: [4, 1], 43: [4, 2], 44: [4, 3], 45: [4, 4], 46: [4, 5], 47: [4, 6], 48: [4, 7], 49: [4, 8], 50: [4, 9],
    51: [5, 0], 52: [5, 1], 53: [5, 2], 54: [5, 3], 55: [5, 4], 56: [5, 5], 57: [5, 6], 58: [5, 7], 59: [5, 8], 60: [5, 9],
    61: [6, 0], 62: [6, 1], 63: [6, 2], 64: [6, 3], 65: [6, 4], 66: [6, 5], 67: [6, 6], 68: [6, 7], 69: [6, 8], 70: [6, 9],
    71: [7, 0], 72: [7, 1], 73: [7, 2], 74: [7, 3], 75: [7, 4], 76: [7, 5], 77: [7, 6], 78: [7, 7], 79: [7, 8], 80: [7, 9],
    81: [8, 0], 82: [8, 1], 83: [8, 2], 84: [8, 3], 85: [8, 4], 86: [8, 5], 87: [8, 6], 88: [8, 7], 89: [8, 8], 90: [8, 9],
    91: [9, 0], 92: [9, 1], 93: [9, 2], 94: [9, 3], 95: [9, 4], 96: [9, 5], 97: [9, 6], 98: [9, 7], 99: [9, 8], 100: [9, 9]
    }

    c_num = -1
    h_num = -1

    # Nhập số lượt đi trước của máy
    clean()
    while not 0 <= c_num <= 50:
        try:
            c_num = int(input('Nhập số nước đi trước của máy (0 <= x <= 50):'))
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    # Nhập các vị trí mà máy đi
    clean()
    for i in range(1, c_num+1):
        render(state, c_choice, h_choice)
        move = 0
        while move < 1 or move > 100:
            try:
                move = int(input(f'Nhập nước đi thứ {i} của máy (1-100): '))
                coord = moves[move]
                can_move = set_move(coord[0], coord[1], COMP)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
        clean()

    # Nhập số lượt đi trước của người
    while  abs(c_num - h_num) >= 2 or h_num < 0:
        try:
            h_num = int(input('Nhập số nước đi trước của người :'))
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Nhập các vị trí mà người đi
    clean()
    for i in range(1, h_num+1):
        render(state, c_choice, h_choice)
        move = 0
        while move < 1 or move > 100:
            try:
                move = int(input(f'Nhập nước đi thứ {i} của người (1-100): '))
                coord = moves[move]
                can_move = set_move(coord[0], coord[1], HUMAN)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
        clean()
    return c_num, h_num

def main():
    """
    Hàm Main gọi các hàm còn lại
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first
    FT = '' # if wanna set first state

    # Người chơi chọn O hoặc X để chơi, nếu chọn khác, in ra "Bad choice" và yêu cầu chọn lại
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Máy O hoặc X - cái còn lại sau khi người chơi chọn
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Người chơi chọn "y" để đặt trạng thái đầu tiên "n" để dùng trạng thái ban đầu mặc định, chọn sai thì yêu cầu chọn lại
    clean()
    while FT != 'Y' and FT != 'N':
        try:
            FT = input('Set first state?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Nếu số lượt đi trước của máy và người bằng nhau thì người chơi phải chọn "y" để đi trước hoặc "n" để máy đi trước
    # Nếu số lượt đi khi đặt trạng thái ban đầu của máy lớn hơn người thì sẽ tới lượt của người đi và ngược lại
    clean()
    if FT == 'Y':
        c_num, h_num = set_FT(board, c_choice, h_choice)
        if c_num == h_num:
            while first != 'Y' and first != 'N':
                try:
                    first = input('First to start?[y/n]: ').upper()
                except (EOFError, KeyboardInterrupt):
                    print('Bye')
                    exit()
                except (KeyError, ValueError):
                    print('Bad choice')
        elif c_num > h_num:
            first = 'Y'
        else:
            first = 'N'
    else:
        # Nếu không đặt trạng thái ban đầu thì chọn "y" để người đi trước hoặc "n" để máy đi trước
        while first != 'Y' and first != 'N':
            try:
                first = input('First to start?[y/n]: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
    clean()

    # Vòng lặp chính của trò chơi, khi trò chơi chưa kết thúc thì thay phiên lượt chơi giữa máy và người
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Thông báo kết thúc trò chơi
    # In "YOU WIN!" nếu người chơi thắng, "YOU LOSE!" nếu người chơi thua., "DRAW!" nếu hòa
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()

# Thực thi hàm main
if __name__ == '__main__':
    main()
