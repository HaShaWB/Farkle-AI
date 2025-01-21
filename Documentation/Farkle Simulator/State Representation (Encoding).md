# State Representation (Encoding)

Game information may include the opponent's scoring history and the score I obtained in the previous turn. Moreover, the state can represent not only my turn but also the opponent's turn. However, to simplify the situation and satisfy the Markov property, the state will represent only my turn. Regardless of the history, only the current score will be included in the data.

## State Data
- **goal**: The target score to win the game.
- **my_point**: The score I have secured so far.
- **temp_point**: The score accumulated during the current turn.
- **opp_point**: The score secured by the opponent.
- **dice_result**: The outcome of the dice roll.

# State Representation Styles
Three representation styles have been defined: **Full data style**, **Dice encoding style**, and **Compact point style**. This project plans to use the second style, **Dice encoding style**.

## 1. Full Data Style
- **goal**, **my_point**, **temp_point**, **opp_point** → Represented as raw scores.
- **dice_result** → Each die is assigned an index and represented as a vector. Excluded dice are represented with 0.

### Result
$$
x = 
\begin{bmatrix}
\text{goal} \\
\text{my point} \\
\text{temp point} \\
\text{opp point} \\
\begin{pmatrix}
\text{dice}_1 \\
\text{dice}_2 \\
\text{dice}_3 \\
\text{dice}_4 \\
\text{dice}_5 \\
\text{dice}_6
\end{pmatrix}
\end{bmatrix}
$$

### Analysis
1. Fully expresses the game situation.
2. The data can be understood directly without special preprocessing or postprocessing.
3. However, including the order of dice results might unnecessarily increase complexity, given the order is meaningless.
4. There is a risk that the model might perceive linear relationships between faces, such as \( \text{face}=1, \text{face}=2, \text{face}=3 \).
5. Hence, a more efficient method to represent dice results led to the next style.

## 2. Dice Encoding Style
- **goal**, **my_point**, **temp_point**, **opp_point** → Represented as raw scores.
- **dice_result** → Encodes the count of each face without considering the order of dice. Excluded dice are automatically handled by this encoding.

### Result
$$
x = 
\begin{bmatrix}
\text{goal} \\
\text{my point} \\
\text{temp point} \\
\text{opp point} \\
\begin{pmatrix}
n(\text{face}=1) \\
n(\text{face}=2) \\
n(\text{face}=3) \\
n(\text{face}=4)\\
n(\text{face}=5) \\
n(\text{face}=6)
\end{pmatrix}
\end{bmatrix}
$$

### Analysis
1. Some information loss occurs.
2. Assuming all dice are equivalent, this loss of information is presumed to be insignificant.
3. Representing dice results independently in separate indices (similar to one-hot encoding in natural language) provides clearer information.

## 3. Compact Point Style
- **my_point** → \( \text{my_point} / \text{goal} \)
- **temp_point** → \( \text{temp_point} / \text{goal} \)
- **opp_point** → \( \text{opp_point} / \text{goal} \)
- **dice_result** → Sorted in ascending order, with excluded dice padded as 0 at the end.

### Result (Example)
$$
x = 
\begin{bmatrix}
\text{my point / goal} \\
\text{temp point / goal} \\
\text{opp point / goal} \\
\begin{pmatrix}
1 \\ 1 \\ 2 \\ 3 \\ 6 \\ 0
\end{pmatrix}
\end{bmatrix}
$$

### Analysis
1. Adaptable to situations where the goal score varies.
2. However, since the dice scores are fixed by the rules, representing the scores inversely proportional to the goal could cause significant information loss.
3. Specifically, while the dice scores change linearly, the value of scores relative to the goal changes nonlinearly, which might introduce significant errors.
