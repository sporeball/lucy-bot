from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
import math
from engine_wrapper import MinimalEngine
from typing import Any
# from enum import Enum

# class Value(Enum):
#   PAWN = 1
#   KNIGHT = 3
#   BISHOP = 3
#   ROOK = 5
#   QUEEN = 9

class ExampleEngine(MinimalEngine):
  pass

class Lucy(ExampleEngine):
  def evaluate(self, board: chess.Board, move) -> float:
    evaluation = 0.0
    moveIsCapture = board.is_capture(move)
    moveIsCheck = board.gives_check(move)
    # captures are good
    if moveIsCapture:
      evaluation += 0.1
    # checks are better
    if moveIsCheck:
      evaluation += 0.5

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
          evaluation -= 0.4
        if board.piece_type_at(response.from_square) == chess.PAWN:
          evaluation -= 0.4

    # pop the move
    board.pop()

    return evaluation

  def search(self, board: chess.Board, *args: Any) -> PlayResult:
    # list of legal moves
    legalMoves = list(board.legal_moves)
    numLegalMoves = len(legalMoves)
    print(f'number of legal moves: {numLegalMoves}')
    # list of options for best move
    bestMoves = []
    # the highest evaluation of any move so far
    maxEvaluation = -math.inf

    if numLegalMoves == 1:
      return PlayResult(bestMoves[0], None)

    # for each move
    for move in legalMoves:
      # evaluate the move
      evaluation = self.evaluate(board, move)
      # if the evaluation is greater than the current maximum,
      # clear the array of best moves, and push this move
      if evaluation > maxEvaluation:
        maxEvaluation = evaluation
        bestMoves = []
        bestMoves.append(move)
      # if the evaluation is equal to the current maximum,
      # push this move to the array of best moves
      elif evaluation == maxEvaluation:
        bestMoves.append(move)

    # randomly select one of the options for best move
    return PlayResult(random.choice(bestMoves), None)
