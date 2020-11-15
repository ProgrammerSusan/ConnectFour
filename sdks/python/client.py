#!/usr/bin/python

import sys
import json
import socket


def get_move(player, board):
    print("-----------------")
    value = minMax(player, board, 2, True)
    print("REEEETURNNN" + value)

    return {"column": value[1]}


def validMove(column, board):
    if board[0][column] != 0:
        return 0


def getMoves(player, board):
    rowIndex = 6
    colIndex = 0
    moves = []
    for row in board[::-1]:
        rowIndex -= 1
        for col in row:
            if col == player:
                if colIndex < 4 and rowIndex > 2:
                    moves.append(searchDiagRightUp(
                        player, board, rowIndex, colIndex))
                if colIndex < 4:
                    moves.append(searchRight(
                        player, board, rowIndex, colIndex))
                if colIndex <= 3 and rowIndex < 4:
                    moves.append(searchDiagRightDown(
                        player, board, rowIndex, colIndex))
                if rowIndex > 2:
                    moves.append(searchUp(
                        player, board, rowIndex, colIndex))
                if colIndex > 2:
                    moves.append(searchDiagLeftUp(
                        player, board, rowIndex, colIndex))
                if colIndex > 2 and rowIndex < 4:
                    moves.append(searchDiagLeftDown(
                        player, board, rowIndex, colIndex))
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
    score = 0
    for col in board[rowIndex]:
        if col == player:
            score += 1
        else:
            if board[rowIndex][colIndex + score] == 0:
                return [score, colIndex + score]
            if board[rowIndex][colIndex + score] != player:
                return [score, -1]


def searchUp(player, board, rowIndex, colIndex):
    score = 1
    i = 1
    while i < 4:
        if board[rowIndex - i][colIndex] == player:
            score += 1
            i += 1
        else:
            i = 5
            if board[rowIndex - score][colIndex] == 0:
                return [score, colIndex]
            if board[rowIndex - score][colIndex] != player:
                return [score, -1]


def searchDiagRightUp(player, board, rowIndex, colIndex):
    # Subtract Rows and add Col
    score = 1
    i = 1
    while i < 4:
        if board[rowIndex - i][colIndex + i] == player:
            score += 1
            i += 1
        else:
            i = 5
            if board[rowIndex - score][colIndex + score] == 0:
                return [score, colIndex]
            if board[rowIndex - score][colIndex + score] != player:
                return [score, -1]


def searchDiagRightDown(player, board, rowIndex, colIndex):
    # Add Rows and add Col
    score = 1
    i = 1
    while i < 4:
        if board[rowIndex + i][colIndex + i] == player:
            score += 1
            i += 1
        else:
            i = 5
            if board[rowIndex + score][colIndex + score] == 0:
                return [score, colIndex]
            if board[rowIndex + score][colIndex + score] != player:
                return [score, -1]


def searchDiagLeftUp(player, board, rowIndex, colIndex):
    # Subtract Rows and subtract Col
    score = 1
    i = 1
    while i < 4:
        if board[rowIndex - i][colIndex - i] == player:
            score += 1
            i += 1
        else:
            i = 5
            if board[rowIndex - score][colIndex - score] == 0:
                return [score, colIndex]
            if board[rowIndex - score][colIndex - score] != player:
                return [score, -1]


def searchDiagLeftDown(player, board, rowIndex, colIndex):
    # Add Rows and add Col
    score = 1
    i = 1
    while i < 4:
        if board[rowIndex - i][colIndex - i] == player:
            score += 1
            i += 1
        else:
            i = 5
            if board[rowIndex - score][colIndex - score] == 0:
                return [score, colIndex]
            if board[rowIndex - score][colIndex - score] != player:
                return [score, -1]


def nextStateBoard(player, board, col, isMax):
    row = 0
    while row < 6:
        if board[row][col] == 0:
            row += 1
    chip = player
    if not isMax:
        if player == 1:
            chip = 2
        else:
            chip = 1
    print(row)
    print(col)
    print(board[6][0])
    board[row][col] = chip
    return board


def minMax(player, board, depth, isMax):
    print("hi")
    if depth == 0:
        print(getMoves(player, board))
        return getMoves(player, board)
    if isMax:
        maxValue = 0

        i = 0
        while i < 7:
            newBoard = nextStateBoard(player, board, i, isMax)
            value = minMax(
                player, newBoard, depth - 1, False)
            maxValue = max(maxValue, value[0])
        return maxValue
    else:
        minValue = 5
        i = 0
        while i < 7:
            newBoard = nextStateBoard(player, board, i, isMax)
            value = minMax(
                player, newBoard, depth - 1, True)
            minValue = min(minValue, value[0])
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
