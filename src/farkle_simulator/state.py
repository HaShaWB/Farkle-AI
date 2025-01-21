# src/farkle_simulator/state.py

from typing import List

class State:
    """
    This class represents the state of a Farkle game in a compact vector form.
    
    According to the docs:
    - goal: The target score to win the game.
    - my_point: The score the current player has secured so far.
    - temp_point: The score accumulated during the current turn.
    - opp_point: The opponent's secured score.
    - dice_result: An integer list where each index corresponds to the count 
      of dice faces (1 through 6).

    The vector representation for this state will be:
    [
      goal, 
      my_point, 
      temp_point, 
      opp_point, 
      n(face=1), 
      n(face=2), 
      n(face=3),
      n(face=4), 
      n(face=5), 
      n(face=6)
    ]

    Note:
    - The first four values (goal, my_point, temp_point, opp_point) are just 
      raw scores (integers).
    - The next six values (dice_result) encode the count of each face (1 to 6).
    - The total length of the returned state vector is 10.
    """
    
    def __init__(self, 
                 goal: int, 
                 my_point: int, 
                 temp_point: int, 
                 opp_point: int, 
                 dice_result_encoded: List[int]) -> None:
        """
        Initialize the State object with the given parameters.

        Args:
            goal (int): The target score to win the game.
            my_point (int): The score the current player has secured.
            temp_point (int): The score accumulated in the current turn.
            opp_point (int): The opponent's secured score.
            dice_result_encoded (List[int]): A list of length 6, where each element 
                represents the count of dice faces from 1 through 6.
        """
        self.goal = goal
        self.my_point = my_point
        self.temp_point = temp_point
        self.opp_point = opp_point
        self.dice_result_encoded = dice_result_encoded

    def to_vec(self) -> List[int]:
        """
        Convert the internal state to a 1D list of length 10.

        Returns:
            List[int]: A list of 10 elements encoding the current game state 
            as described in the class docstring:
              [
                goal,
                my_point,
                temp_point,
                opp_point,
                n(face=1),
                n(face=2),
                n(face=3),
                n(face=4),
                n(face=5),
                n(face=6)
              ]
        """
        return [
            self.goal,
            self.my_point,
            self.temp_point,
            self.opp_point,
            *self.dice_result_encoded
        ]
