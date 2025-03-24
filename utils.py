def get_valid_int(prompt):
    """Prompt the user for an integer input and validate it. 
       If the user presses Enter, return to the menu.

    Args:
        prompt (str): The message displayed to the user.

    Returns:
        int: The validated integer input, or None if the user presses Enter.
    """
    while True:
        user_input = input(prompt).strip()

        if user_input == "":
            print("Returning to the menu...")
            return None  # Return to the menu

        if user_input.isdigit():
            return int(user_input)  

        print("Invalid input. Please enter a valid numeric ID.")


def get_valid_float(prompt, decimal_places=2):
    """Prompts the user for a float value, ensuring it has the correct number of decimal places."""
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input == "":
                print("Input cannot be empty.")
                continue
            
            value = float(user_input)
            if round(value, decimal_places) != value:
                raise ValueError(f"Value must have up to {decimal_places} decimal places.")
            
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")
            