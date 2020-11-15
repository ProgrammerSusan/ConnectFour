#!/usr/bin/python

import sys
import json
import socket
import copy


def get_move(player, board):
    #print("inital board", board)
    # print(board[0][0])
    value = minMax(player, board, 2, True)

    return {"column": value[1]}


def validMove(column, board):
    #print("valid move column ", column)
    if board[0][column] != 0:
        return False
    else:
        return True


def getMoves(player, board):
    moves = []
    col = 0
    while col < 7:
        row = 0
        #print("column getMoves ", col)
        yes = validMove(col, board)
        #print("Is the move valid? ", yes)
        # print(True)
        if validMove(col, board):
            while row < 5:
                if board[row][col] == 0 and board[row + 1][col] != 0:
                    moves.append(searchDiagRightUp(player, board, row, col))
                    moves.append(searchRight(player, board, row, col))
                    moves.append(searchLeft(player, board, row, col))
                    moves.append(searchDiagRightDown(player, board, row, col))
                    moves.append(searchDown(player, board, row, col))
                    moves.append(searchDiagLeftUp(player, board, row, col))
                    moves.append(searchDiagLeftDown(player, board, row, col))
                row += 1

            moves.append(searchDiagRightUp(player, board, 5, col))
            moves.append(searchRight(player, board, 5, col))
            moves.append(searchLeft(player, board, 5, col))
            moves.append(searchDiagRightDown(player, board, 5, col))
            moves.append(searchDown(player, board, 5, col))
            moves.append(searchDiagLeftUp(player, board, 5, col))
            moves.append(searchDiagLeftDown(player, board, 5, col))
        else:
            return [-1, col]
        col += 1
    return getBestMove(moves)


def getBestMove(moves):
    max = 0
    bestMove = []
    for score, col in moves:
        if score > max:
            max = score
            bestMove = [score, col]
    return bestMove


def searchRight(player, board, rowIndex, colIndex):
    score = 1
    i = 1
    while i < 4 and (colIndex + i < 7):
        if board[rowIndex][colIndex + i] == player:
            score += 1
            i += 1
        else:
            return [scoreMove(score, colIndex), colIndex]
    return [scoreMove(score, colIndex), colIndex]


def searchLeft(player, board, rowIndex, colIndex):
    score = 1
    i = 1
    while i < 4 and (colIndex - i >= 0):
        if board[rowIndex][colIndex - i] == player:
            score += 1
            i += 1
        else:
            return [scoreMove(score, colIndex), colIndex]
    return [scoreMove(score, colIndex), colIndex]


def searchDown(player, board, rowIndex, colIndex):
    score = 1
    i = 1
    while i < 4 and (rowIndex + i < 6):
        if board[rowIndex + i][colIndex] == player:
            score += 1
            i += 1
        else:
            return [scoreMove(score, colIndex), colIndex]
    return [scoreMove(score, colIndex), colIndex]


def searchDiagRightUp(player, board, rowIndex, colIndex):
    # Subtract Rows and add Col
    score = 1
    i = 1
    while i < 4 and (rowIndex - i >= 0 and colIndex + i < 7):
        if board[rowIndex - i][colIndex + i] == player:
            score += 1
            i += 1
        else:
            return [scoreMove(score, colIndex), colIndex]
    return [scoreMove(score, colIndex), colIndex]


def searchDiagRightDown(player, board, rowIndex, colIndex):
    # Add Rows and add Col
    score = 1
    i = 1
    while i < 4 and (rowIndex + i < 6 and colIndex + i < 7):
        if board[rowIndex + i][colIndex + i] == player:
            score += 1
            i += 1
        else:
            return [scoreMove(score, colIndex), colIndex]
    return [scoreMove(score, colIndex), colIndex]


def searchDiagLeftUp(player, board, rowIndex, colIndex):
    # Subtract Rows and subtract Col
    score = 1
    i = 1
    while i < 4 and (rowIndex - i >= 0 and colIndex - i >= 0):
        if board[rowIndex - i][colIndex - i] == player:
            score += 1
            i += 1
        else:
            return [scoreMove(score, colIndex), colIndex]
    return [scoreMove(score, colIndex), colIndex]


def searchDiagLeftDown(player, board, rowIndex, colIndex):
    # Add Rows and add Col
    score = 1
    i = 1
    while i < 4 and (rowIndex + i < 6 and colIndex - i >= 0):
        if board[rowIndex + i][colIndex - i] == player:
            score += 1
            i += 1
        else:
            return [scoreMove(score, colIndex), colIndex]
    return [scoreMove(score, colIndex), colIndex]


def scoreMove(score, colIndex):
    if score == 3:
        score *= 100
    if score == 2:
        score *= 15
    if colIndex == 3:
        score *= 10
    if colIndex == 2 or colIndex == 4:
        score *= 5
    if colIndex == 1 or colIndex == 5:
        score *= 2
    return score


def nextStateBoard(player, board, col, isMax):

    chip = player
    if not isMax:
        if player == 1:
            chip = 2
        else:
            chip = 1
    print(chip)

    #print("before", board)
    board = copy.deepcopy(board)
    for row in board[::-1]:
        if row[col] == 0:
            print(row)
            row[col] = chip
            return board
    return board


def minMax(player, board, depth, isMax):
    if depth == 0:
        #print(getMoves(player, board))
        #print("depth", depth)
        #print("initial board", board)
        return getMoves(player, board)
    if isMax:
        maxValue = [0, 3]

        for i in range(0, 7):
            #newBoard = copy.deepcopy(board)
            newBoard = nextStateBoard(player, board, i, isMax)
            print("newboard ", newBoard)
            value = minMax(
                player, newBoard, depth, False)
            if maxValue[0] < value[0]:
                maxValue = value

        #print("maxValue ", maxValue)
        return maxValue
    else:
        minValue = [1000000, 3]
        for i in range(0, 7):
            #print("depthmin ", depth)
            #newBoard = copy.deepcopy(board)
            newBoard = nextStateBoard(player, board, i, isMax)
            value = minMax(
                player, newBoard, depth - 1, True)
            if minValue[0] > value[0] and value[0] > 0:
                minValue = value
        #print("minValue ", minValue)
        return minValue


def prepare_response(move):
    response = '{}\n'.format(json.dumps(move))
    print('sending {!r}'.format(response))
    return response


if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
    host = sys.argv[2] if (
        len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        while True:
            data = sock.recv(1024)
            if not data:
                print('connection to server closed')
                break
            json_data = json.loads(str(data.decode('UTF-8')))
            board = json_data['board']
            maxTurnTime = json_data['maxTurnTime']
            player = json_data['player']
            print(player, maxTurnTime, board)

            move = get_move(player, board)
            response = prepare_response(move)
            sock.sendall(response)
    finally:
        sock.close()
