from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
from engine_wrapper import MinimalEngine
from typing import Any

class ExampleEngine(MinimalEngine):
  pass

class Lucy(ExampleEngine):
  def evaluate(self, board: chess.Board, move) -> float:
    ev = 0.0
    isCapture = board.is_capture(move)
    isCheck = board.gives_check(move)
    # board.push(move)
    # board.pop()
    if isCapture:
      ev += 0.1
    if isCheck:
      ev += 0.5
    return ev

  def search(self, board: chess.Board, *args: Any) -> PlayResult:
    # list of legal moves
    legalMoves = list(board.legal_moves)
    # list of options for best move
    bestMoves = []
    # the highest evaluation of any move so far
    maxEv = 0.0

    # for each move
    for move in legalMoves:
      # evaluate the move
      ev = self.evaluate(board, move)
      # if the evaluation is greater than the current maximum,
      # clear the array of best moves, and push this move
      if ev > maxEv:
        maxEv = ev
        bestMoves = []
        bestMoves.append(move)
      # if the evaluation is equal to the current maximum,
      # push this move to the array of best moves
      elif ev == maxEv:
        bestMoves.append(move)

    # randomly select one of the options for best move
    return PlayResult(random.choice(bestMoves), None)
