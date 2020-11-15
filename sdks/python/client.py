#!/usr/bin/python

import sys
import json
import socket


def get_move(player, board):
    print("-----------------")
    value = minMax(player, board, 2, True)
    print("REEEETURNNN", value)

    return {"column": value[1]}


def validMove(column, board):
    if board[0][column] != 0:
        return 0


def getMoves(player, board):
    moves = []
    for col in range(0, len(board[0])):
        for row in range(0, 6):
            if board[row][col] == 0 and (row < 5 and board[row + 1][col] != 0):
                moves.append(searchDiagRightUp(player, board, row, col))
                moves.append(searchRight(player, board, row, col))
                moves.append(searchLeft(player, board, row, col))
                moves.append(searchDiagRightDown(player, board, row, col))
                moves.append(searchDown(player, board, row, col))
                moves.append(searchDiagLeftUp(player, board, row, col))
                moves.append(searchDiagLeftDown(player, board, row, col))
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
            return [score, colIndex]
    return [score, colIndex]

def searchLeft(player, board, rowIndex, colIndex):
    score = 1
    i = 1
    while i < 4 and (colIndex - i >= 0):
        if board[rowIndex][colIndex - i] == player:
            score += 1
            i += 1
        else:
            return [score, colIndex]
    return [score, colIndex]


def searchDown(player, board, rowIndex, colIndex):
    score = 1
    i = 1
    while i < 4 and (rowIndex + i < 6):
        if board[rowIndex + i][colIndex] == player:
            score += 1
            i += 1
        else:
            return [score, colIndex]
    return [score, colIndex]


def searchDiagRightUp(player, board, rowIndex, colIndex):
    # Subtract Rows and add Col
    score = 1
    i = 1
    while i < 4 and (rowIndex - i >= 0 and colIndex + i < 7):
        if board[rowIndex - i][colIndex + i] == player:
            score += 1
            i += 1
        else:
            return [score, colIndex]
    return [score, colIndex]


def searchDiagRightDown(player, board, rowIndex, colIndex):
    # Add Rows and add Col
    score = 1
    i = 1
    while i < 4 and (rowIndex + i < 6 and colIndex + i < 7):
        if board[rowIndex + i][colIndex + i] == player:
            score += 1
            i += 1
        else:
            return [score, colIndex]
    return [score, colIndex]


def searchDiagLeftUp(player, board, rowIndex, colIndex):
    # Subtract Rows and subtract Col
    score = 1
    i = 1
    while i < 4 and (rowIndex - i >= 0 and colIndex - i >= 0):
        if board[rowIndex - i][colIndex - i] == player:
            score += 1
            i += 1
        else:
            return [score, colIndex]
    return [score, colIndex]


def searchDiagLeftDown(player, board, rowIndex, colIndex):
    # Add Rows and add Col
    score = 1
    i = 1
    while i < 4 and (rowIndex + i < 6 and colIndex - i >= 0):
        if board[rowIndex + i][colIndex - i] == player:
            score += 1
            i += 1
        else:
            return [score, colIndex]
    return [score, colIndex]


def nextStateBoard(player, board, col, isMax):
    row = 0
    while row < 5 and board[row + 1][col] == 0:
        row += 1

    chip = player
    if not isMax:
        if player == 1:
            chip = 2
        else:
            chip = 1
    board[row][col] = chip
    return board


def minMax(player, board, depth, isMax):
    if depth == 0:
        print(getMoves(player, board))
        print("depth", depth)
        return getMoves(player, board)
    if isMax:
        maxValue = [0, 3]

        for i in range(0,7):
            print("in the max loop")
            print(i)
            print("depth max ", depth)
            newBoard = nextStateBoard(player, board, i, isMax)
            value = minMax(
                player, newBoard, depth, False)
            # still not conviced that this is an array
            if maxValue[0] < value[0]:
                maxValue = value
        return maxValue
    else:
        minValue = [5, 3]
        for i in range(0, 7):
            print("depthmin ", depth)
            newBoard = nextStateBoard(player, board, i, isMax)
            value = minMax(
                player, newBoard, depth - 1, True)
            # print("minValue ", minValue)
            # print("value ", value)
            if minValue[0] > value[0]:
                minValue = value
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
