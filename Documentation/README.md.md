A Python-JAX-based reinforcement learning agent designed to master the Farkle dice game, leveraging advanced RL algorithms for strategy optimization and gameplay enhancement.

---
## What is Farkle

Farkle is a classic dice game played with six dice, where players compete to score points by rolling specific combinations. The game blends elements of strategy, risk management, and probability, making it a fun yet challenging experience. The primary goal is to reach a predetermined score, typically 10,000 points, before your opponent.

---
## [[Farkle Rules]]

1. **Scoring Points**: Roll the dice to create specific combinations that score points. For example, a single "1" scores 100 points, a "5" scores 50 points, and three of the same number provide additional points.
2. **Choosing Additional Rolls**: Decide whether to roll the remaining dice after scoring some, aiming to increase your total points.
3. **Farkle**: If no scoring combination appears after a roll, it is called a "Farkle," and all points accumulated during that turn are lost.
4. **Winning the Game**: The first player to reach the target score (e.g., 10,000 points) wins the game.

Farkle is simple in its rules, yet its core lies in evaluating risks and making strategic decisions on every turn.

---
## Development

- **Farkle Simulator**
    - Score Calculator: Takes dice results and selected dice as input and returns the score.
    - State Class:
        - Target Score: The score required to win the game (e.g., 10,000 points).
        - Player's Total Score: The score the player has "secured."
        - Opponent's Total Score: The score the opponent has "secured."
        - Temporary Player Score: The score temporarily accumulated during the player's turn.
        - Dice Roll Results: The outcome of the dice roll.
    - Next State Function: Takes a state object and a decision vector as input, and returns the next state object and the corresponding score.
- **Farkle Agent**
    - Takes a state object as input and returns a decision vector.
- **Training**
    - Two Farkle Agents play against each other and learn through self-play.


---
## Project Objective

The goal of this project is to develop a reinforcement learning agent capable of playing the game of Farkle. Through this development process, we aim to observe how the agent learns strategic decision-making and gain a deeper understanding of the core principles and mechanisms of reinforcement learning.

By training the agent in an environment that combines uncertainty and risk management, we explore how it incrementally learns optimal policies. This project serves as a practical example of how reinforcement learning works and can be applied, making it a valuable resource for both researchers and learners.