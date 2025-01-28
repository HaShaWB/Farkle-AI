from typing import List, Tuple


def calculate_farkle_score(dice_result: List[int],
                           selection: List[int],
                           roll_over: bool) -> Tuple[int, bool]:
    """
    Calculate the Farkle score based on the provided dice counts (dice_result),
    the user's chosen selection (selection), and whether the user intends to
    roll again or end the turn (roll_over).

    This implementation follows the scoring rules described in the docs:

    1. Selection Validation:
       - If no dice are selected:
         - If roll_over = False: return (0, False).
         - If roll_over = True : return (-1000, False).
       - If selection is not a valid subset of dice_result: return (-1000, False).

    2. Check 6 of a Kind:
       - If found, return immediately with the corresponding score.
         * If face = 1, score = 1000 * (2^3).
         * Otherwise, face_value * 100 * (2^3).

    3. Check 5 of a Kind:
       - If found, add the corresponding score to p, reduce selection, continue.
         * If face = 1, add 1000 * (2^2).
         * Otherwise, face_value * 100 * (2^2).

    4. Check 4 of a Kind:
       - If found, add the corresponding score to p, reduce selection, continue.
         * If face = 1, add 1000 * 2.
         * Otherwise, face_value * 100 * 2.

    5. Check 3 of a Kind (Repeat twice):
       - Up to two times, if found, add corresponding score, reduce selection, continue.
         * If face = 1, add 1000.
         * Otherwise, face_value * 100.

    6. Check Large Straight (6 consecutive):
       - If all selection[i] == 1 for i in [0..5], return (2500, roll_over).

    7. Check Small Straight (5 consecutive):
       - If selection meets [1,1,1,1,1,0] or [0,1,1,1,1,1],
         add 1000 to p, reduce the used dice by 1, continue.

    8. Check Three Pairs:
       - If exactly three distinct faces have selection[i] == 2, return (1500, roll_over).

    9. Calculate Remaining Single 1s and 5s:
       - Add 100 * selection[0] (face=1), add 50 * selection[4] (face=5).

    10. Check if all selected dice are consumed (selection == 0-vector):
       - If p == 0 and roll_over == False, return (0, False).
       - If p == 0 and roll_over == True, return (-1000, False).
       - Otherwise, return (p, roll_over).

    11. If some dice remain in 'selection' after all these steps, return (0, False).
        (Because not all dice were scored)

    :param dice_result: List[int]
                       A 6-dimensional list, where dice_result[i] represents the
                       count of (i+1)-face dice in the roll.
    :param selection:   List[int]
                       A 6-dimensional list, where selection[i] represents the
                       count of (i+1)-face dice chosen by the player.
    :param roll_over:   bool
                       Whether the player chooses to roll the remaining dice (True)
                       or end their turn (False).
    :return:            Tuple[int, bool]
                       The first element is the score for this selection.
                       The second element is the roll_over decision (possibly overridden).
    """
    # p will accumulate the score for the current selection
    p = 0

    # 1. Selection Validation
    if sum(selection) == 0:
        # Case: No dice selected
        if not roll_over:
            # End turn with no points
            return (0, False)
        else:
            # Penalty for rolling over with no selection
            return (-1000, False)

    # Check if 'selection' is a valid subset of 'dice_result'
    for i in range(6):
        if selection[i] < 0 or selection[i] > dice_result[i]:
            # Invalid selection => penalty
            return (-1000, False)

    # 2. Check 6 of a Kind
    for i in range(6):
        if selection[i] == 6:
            # If face == 1
            if i == 0:
                return (1000 * (2 ** 3), roll_over)  # 1,000 * 8 = 8,000
            else:
                return ((i + 1) * 100 * (2 ** 3), roll_over)  # face * 100 * 8
    # If not found, proceed

    # 3. Check 5 of a Kind
    for i in range(6):
        if selection[i] == 5:
            if i == 0:
                p += 1000 * (2 ** 2)  # 1,000 * 4 = 4,000
            else:
                p += (i + 1) * 100 * (2 ** 2)  # face * 100 * 4
            selection[i] -= 5
            break  # Only one 5-of-a-kind can exist in 6 dice

    # 4. Check 4 of a Kind
    for i in range(6):
        if selection[i] == 4:
            if i == 0:
                p += 1000 * 2  # 2,000
            else:
                p += (i + 1) * 100 * 2
            selection[i] -= 4
            break  # Only one 4-of-a-kind can exist

    # 5. Check 3 of a Kind (Repeat Twice)
    for _ in range(2):
        found_three = False
        for i in range(6):
            if selection[i] == 3:
                if i == 0:
                    p += 1000
                else:
                    p += (i + 1) * 100
                selection[i] -= 3
                found_three = True
                break
        if not found_three:
            break

    # 6. Check Large Straight (1-2-3-4-5-6)
    # All selection[i] == 1
    if all(s == 1 for s in selection):
        return (2500, roll_over)

    # 7. Check Small Straight (two forms)
    # (1,2,3,4,5) => selection[0..4] == 1 or (2,3,4,5,6) => selection[1..5] == 1
    # If found, add 1000 and reduce those dice by 1
    if selection[0] == 1 and selection[1] == 1 and selection[2] == 1 and \
            selection[3] == 1 and selection[4] == 1 and selection[5] == 0:
        p += 1000
        for i in range(5):
            selection[i] -= 1
    elif selection[0] == 0 and selection[1] == 1 and selection[2] == 1 and \
            selection[3] == 1 and selection[4] == 1 and selection[5] == 1:
        p += 1000
        for i in range(1, 6):
            selection[i] -= 1

    # 8. Check Three Pairs
    # If exactly three faces have selection[i] == 2
    if sum(1 for i in range(6) if selection[i] == 2) == 3:
        return (1500, roll_over)

    # 9. Remaining Dice (Single 1s and 5s)
    # face=1 => index=0, face=5 => index=4
    if selection[0] > 0:
        p += 100 * selection[0]
        selection[0] = 0
    if selection[4] > 0:
        p += 50 * selection[4]
        selection[4] = 0

    # 10. Check for Full Consumption
    if all(s == 0 for s in selection):
        # All selected dice are consumed
        if p == 0:
            # If no points from selection
            if roll_over:
                # Penalty for rolling over with no real points
                return (-1000, False)
            else:
                # Farkle with no score
                return (0, False)
        else:
            # Some points are gained successfully
            return (p, roll_over)
    else:
        # If not all dice are consumed, no valid final
        return (-1000, False)
