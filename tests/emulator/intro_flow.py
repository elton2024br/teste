"""Recorded inputs for the Amazon intro, ending inside the player's house."""


def advance(count=1, wait=300):
    return (f"run 1 30\nrun 0 {wait}\n") * count


def intro_to_gender():
    commands = "run 0 300\nrun 8 20\nrun 0 100\n"
    commands += advance(wait=180) + advance(2, 90) + advance(wait=420)
    commands += advance(wait=240) + advance(8)
    return commands


def new_game(gender=0, reject_name=False, empty_name=False):
    commands = intro_to_gender()
    if gender:
        commands += "run 128 12\nrun 0 30\n"
    # Choose appearance, enter A as a custom name, then confirm with START/OK.
    commands += advance()
    if not empty_name:
        commands += advance()
    commands += "run 8 20\nrun 0 30\n" + advance()
    if reject_name:
        commands += "run 128 12\nrun 0 30\n" + advance()
        # NO opens a fresh keyboard. Enter B to prove the first name was rejected.
        commands += "run 16 12\nrun 0 30\n" + advance()
        commands += "run 8 20\nrun 0 30\n" + advance()
    commands += advance(wait=360) + advance(5) + advance(wait=500)
    return commands
