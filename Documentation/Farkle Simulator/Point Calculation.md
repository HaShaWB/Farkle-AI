# Point Calculation

This document explains the logic for calculating scores in the game of Farkle based on the given state and a player's selection.

## Major Logic

- `dice result` ($X$): A 6-dimensional vector representing the count of dice faces rolled (1 through 6).
- `selection` ($S$): A 6-dimensional vector representing the count of dice faces selected by the player.
- `number of selection` (#): The total count of dice selected in $S$.
- `roll_over` ($r'$): A boolean indicating whether the player chooses to roll the remaining dice or end their turn.
- `result space` ($\mathbf J_6$): The set of possible dice faces {1, 2, 3, 4, 5, 6}.
- `temp_point` ($p$): The points calculated during the current turn.
- `return` ($R(p, r')$): A tuple returning the calculated points $p$ and the roll_over decision $r'$.

---

### 1. Selection Validation
1. **Check if any dice were selected**  
$$
S = \mathbf 0
$$
- `True`:  
	- If $r' = 0$, return $R(0, 0)$ (end turn with no points).  
	- If $r' = 1$, return $R(-1000, 0)$ (penalty for rolling over with no points).  
- `False`: Proceed.

2. **Check if the selection is valid**  
   Validate whether $S$ is a subset of $X$:  
$$
\bigwedge_{i \in \mathbf J_6} (X[i] - S[i] \geq 0) \quad \text{and} \quad \forall i \in \mathbf J_6, 0 \leq S[i]
$$
- `True`: Proceed.  
- `False`: Return $R(-1000, 0)$ (penalty for invalid selection).  

---

### 2. Check 6 of a Kind
$$
\exists i \in \mathbf J_6, \; S[i] = 6
$$
- `True`:  
	- If $i = 1$, return $R(p = 1000 \times 2^3, r')$.  
	- If $i \neq 1$, return $R(p = i \times 100 \times 2^3, r')$.  
- `False`: Proceed.

---

### 3. Check 5 of a Kind
$$
\exists i \in \mathbf J_6, \; S[i] = 5
$$
- `True`:  
	- If $i = 1$, update $p \leftarrow (p + 1000 \times 2^2)$ and $S[i] \leftarrow (S[i] - 5)$.  
	- If $i \neq 1$, update $p \leftarrow (p + i \times 100 \times 2^2)$ and $S[i] \leftarrow (S[i] - 5)$.  
- `False`: Proceed.

---

### 4. Check 4 of a Kind
$$
\exists i \in \mathbf J_6, \; S[i] = 4
$$
- `True`:  
	- If $i = 1$, update $p \leftarrow (p + 1000 \times 2)$ and $S[i] \leftarrow (S[i] - 4)$.  
	- If $i \neq 1$, update $p \leftarrow (p + i \times 100 \times 2)$ and $S[i] \leftarrow (S[i] - 4)$.  
- `False`: Proceed.

---

### 5. Check 3 of a Kind (Repeat Twice)
$$
\exists i \in \mathbf J_6, \; S[i] = 3
$$
- `True`:  
  - If $i = 1$, update $p \leftarrow (p + 1000)$ and $S[i] \leftarrow (S[i] - 3)$.  
  - If $i \neq 1$, update $p \leftarrow (p + i \times 100)$ and $S[i] \leftarrow (S[i] - 3)$.  
- `False`: Proceed.

---

### 6. Large Straight
$$
\forall i \in \mathbf J_6, \; S[i] = 1
$$
- `True`: Return $R(2500, r')$.  
- `False`: Proceed.

---

### 7. Small Straight
$$
\big((1 \leq i \leq 5 \implies S[i] = 1) \; \lor \; (2 \leq i \leq 6 \implies S[i] = 1)\big)
$$
- `True`: Update $p \leftarrow (p + 1000)$ and reduce the corresponding $S[i]$ values by 1.  
- `False`: Proceed.

---

### 8. Three Pairs
$$
n(\{i:S[i] = 2\}) = 3
$$
- `True`: Return $R(1500, r')$
- `False`: Proceed.

---
### 9. Remaining Dice (Single 1s and 5s)
- Update $p \leftarrow (p + 100 \times S[1])$ and set $S[1] \leftarrow 0$.  
- Update $p \leftarrow (p + 50 \times S[5])$ and set $S[5] \leftarrow 0$.

---

### 10. Check for Full Consumption
$$
\forall i \in \mathbf J_6,\; S[i] = 0
$$
- `True`:  
	- If $p = 0 \land r' = 0$, return $R(0, 0)$ (Farkle).  
	- If $p = 0 \land r' = 1$, return $R(-1000, 0)$ (penalty for rolling over with no points).  
	- If $p \neq 0$, return $R(p, r')$.
- `False`: Return $R(0, 0)$.
