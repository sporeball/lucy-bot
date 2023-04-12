from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
import math
from engine_wrapper import MinimalEngine
from typing import Any

class ExampleEngine(MinimalEngine):
  pass

class Lucy(ExampleEngine):
  def evaluate(self, board: chess.Board, move) -> float:
    ev = 0.0
    moveIsCapture = board.is_capture(move)
    moveIsCheck = board.gives_check(move)
    # captures are good
    if moveIsCapture:
      ev += 0.1
    # checks are better
    if moveIsCheck:
      ev += 0.5

    # push the move
    board.push(move)

    # get list of the opponent's responses
    legalResponses = list(board.legal_moves)
    # if the move Lucy played is a check,
    # for each response,
    if moveIsCheck:
      for response in legalResponses:
        # if the response is a capture by something other than the king,
        # or the response's source square has a pawn on it,
        # it might not be a good idea to play that check
        if (
          board.is_capture(response) and
          board.piece_type_at(response.from_square) != chess.KING
        ):
          ev -= 0.4
        if board.piece_type_at(response.from_square) == chess.PAWN:
          ev -= 0.4

    # pop the move
    board.pop()

    return ev

  def search(self, board: chess.Board, *args: Any) -> PlayResult:
    # list of legal moves
    legalMoves = list(board.legal_moves)
    numLegalMoves = len(legalMoves)
    print(f'number of legal moves: {numLegalMoves}')
    # list of options for best move
    bestMoves = []
    # the highest evaluation of any move so far
    maxEv = -math.inf

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
