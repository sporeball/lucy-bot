"""
Some example strategies for people who want to create a custom, homemade bot.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
from engine_wrapper import MinimalEngine
from typing import Any


class ExampleEngine(MinimalEngine):
    pass

class Lucy(ExampleEngine):
  """RandomMove"""
  def search(self, board: chess.Board, *args: Any) -> PlayResult:
    return PlayResult(random.choice(list(board.legal_moves)), None)
