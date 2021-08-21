from math import inf as infinity
from random import choice
import platform
import time
from os import system


HUMAN = -1
COMP = +1

# Trạng thái ban đầu của bảng (ma trận 3x3) khi chưa chơi
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
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
    * Ba hàng ngang   [X X X] or [O O O]
    * Ba cột dọc      [X X X] or [O O O]
    * Hai đường chéo  [X X X] or [O O O]
    :param state : trạng thái hiện tại của bảng
    :param player : nhận giá trị là HUMAN (người chơi) hoặc COMP (máy tính)
    :return: Trả về True nếu player thắng, ngược lại trả về False
    """
    # Ma trận này chứa các khả năng chiến thắng của player
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
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
    str_line = '---------------'

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
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
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
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    # Xóa mà hình console cũ
    clean()

    # In màn hình console hiện tại
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    # Người chơi nhập nước đi của mình, nếu nước đi không hợp lệ, in ra "Bad choice" và yêu cầu nhập lại
    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
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
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    c_num = -1
    h_num = -1

    # Nhập số lượt đi trước của máy
    clean()
    while not 0 <= c_num <= 4:
        try:
            c_num = int(input('Nhập số nước đi trước của máy (0 <= x <= 4):'))
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
        while move < 1 or move > 9:
            try:
                move = int(input(f'Nhập nước đi thứ {i} của máy (1-9): '))
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
        while move < 1 or move > 9:
            try:
                move = int(input(f'Nhập nước đi thứ {i} của người (1-9): '))
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
