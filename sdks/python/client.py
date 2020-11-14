#!/usr/bin/python

import sys
import json
import socket


def get_move(player, board):
    # TODO determine valid moves
    # TODO determine best move
    return {"column": 1}


def validMove(column, board):
    if board[0][column] != 0:
        return 0


def prepare_response(move):
    response = '{}\n'.format(json.dumps(move))
    print('sending {!r}'.format(response))
    return response


if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

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

def getBestMove(player, board):
    var rowIndex = 6
    var colIndex = 0
    for row in board[::-1]:
        rowIndex -= 1
        for col in row:
            if col == player:
            col += 1
    return

def searchRight(player, board, rowIndex, colIndex):
    var score = 0
    for col in board[rowIndex]:
        if col == player:
            score += 1
        else:
            if board[rowIndex][colIndex + score] == 0:
                return [score, colIndex + score]
            if board[rowIndex][colIndex + score] != player:
                return [score, -1]

def searchUp(player, board, rowIndex, colIndex):
    var score = 1
    var i = 1
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
    ## Subtract Rows and add Col
    var score = 1
    var i = 1
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
    ## Add Rows and add Col
    var score = 1
    var i = 1
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
    ## Subtract Rows and subtract Col
    var score = 1
    var i = 1
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
    ## Add Rows and add Col
    var score = 1
    var i = 1
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
