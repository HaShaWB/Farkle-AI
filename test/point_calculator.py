import json

from src.farkle_simulator.point_calculator import calculate_farkle_score


try:
    examples = json.load(open("point_examples.jsonl"))
except:
    examples = []

while True:

    dice_result = input("Enter a result: ")
    dice_result = dice_result.split()
    dice_result = list(map(int, dice_result))

    selection = input("Enter a selection: ")
    selection = selection.split()
    selection = list(map(int, selection))

    roll_over = input("Enter a roll over (y/n): ")
    roll_over = False if roll_over.lower() == "n" else True

    actual_score = input("Enter an actual score: ")
    actual_score = int(actual_score)

    predicted_score = calculate_farkle_score(dice_result, selection, roll_over)

    exam_case = {
        "dice result": dice_result,
        "selection": selection,
        "roll over": roll_over,
        "predicted score": predicted_score,
        "actual score": actual_score
    }

    examples.append(exam_case)

    with open("point_examples.jsonl", "w") as f:
        for example in examples:
            f.write(json.dumps(example) + "\n")

    exam_str = ""

    for key, value in exam_case.items():
        exam_str += f"{key}: {value}\n"

    exam_str += "**------------------------------------------**\n"
    print(exam_str)
