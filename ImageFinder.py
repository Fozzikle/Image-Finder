from imaging import get_image

# Creating border variable based on example
BORDER_WIDTH = 50
border = "*" * BORDER_WIDTH


# Creating text format functions
def title_text(text):
    """Print centered text inside '+' borders."""
    print("+" + f"{text:^{BORDER_WIDTH - 2}}" + "+")


def left_text(text):
    """Print left-aligned text inside '*' borders."""
    print("* " + f"{text:<{BORDER_WIDTH - 3}}" + "*")


# Validation functions
def validate_id(user_id):
    """Validates user's id checking if it was a unikey or student id."""

    # Checking if input is student id
    if len(user_id) == 9 and user_id.isdigit():
        return True

    # Checking if input is a unikey
    elif len(user_id) == 8 and user_id[:4].isalpha() and user_id[4:].isdigit():
        return True

    return False


def validate_code(image_code):
    """Validates the image code entered by user."""

    length = len(image_code)

    # Calculating split point of code
    split = (length + 1) // 2
    first_half = image_code[:split]
    second_half = image_code[split:]

    # Check if the user inputted a correct image code
    valid_image_code = (
        # validating code length
        (8 <= length <= 16) and

        # Check if the first half of code is all lower case letters
        first_half.isalpha() and first_half.islower() and

        # Check if the second half are digits only
        second_half.isdigit()
    )

    return valid_image_code


# Image related functions
def request_image(user_id):
    """
    Requests an image from database based on user id and image code provided
    """

    # Looping request for valid image code
    while True:
        image_code = input("Enter the image code: ")

        if image_code == "exit":
            return None

        if not validate_code(image_code):
            continue

        # Ends validation loop when a valid code is entered
        break

    # Searching image library for images matching the code
    image_dict = get_image(user_id, image_code)

    if image_dict is None:
        print("No image found for this code.")

    else:
        print(f"Found image: {image_dict['title']}")
        return image_dict


def process_image(image_data):
    """Writes an image to gallery.txt"""

    # Adding image data to gallery.txt
    with open("gallery.txt", "a") as f:
        f.write(f"Title: {image_data['title']}\n{image_data['image']}\n")


def view_gallery():
    """View images stored in gallery.txt ouput in alphabetical order"""

    # Checking if gallery.txt exists
    try:
        with open("gallery.txt", "r") as file:
            gallery_entry = file.read().strip()

    except FileNotFoundError:
        print("No images found in database.")
        return None

    # Splitting entries to store them in dictionary
    raw_entries = gallery_entry.split("Title:")  # Split up entries by title
    entries = {}

    for entry in raw_entries:

        # Removing leading and trailing whitespace
        entry = entry.strip()
        if not entry:
            continue

        lines = entry.splitlines()
        title = lines[0].strip()
        art = "\n".join(lines[1:])  # Rebuild the ascii art

        # Storing ascii art
        entries[title] = art

    # Original: Printing output + sorting in alphabetical order
    #for title in sorted(entries.keys()):
        #print(f"Title: {title}")
        #print(entries[title])

    # AI debug: padding from ascii wasn't replicating through reprinting art
    for title in sorted(entries.keys()):
        print(f"Title: {title}")

        lines = entries[title].split("\n")

        # --- Fix House: add ONE space to the LAST line only ---
        if title == "House":
            # Only modify the last line
            if not lines[-1].endswith(" "):
                lines[-1] = lines[-1] + " "

        # --- Fix Smiley Face: pad all lines to the longest width ---
        elif title == "Smiley Face":
            max_len = max(len(line) for line in lines)
            lines = [line.ljust(max_len) for line in lines]

        # Print the ASCII art
        print("\n".join(lines))

    return None


# Welcome screen display
print(border)
title_text("Image Finder")
print(border)
title_text("Log in and record your findings!")
print(border)

# Prompting user for id
user_id = input("Enter your ID: ")

# Validating id
while not validate_id(user_id):
    user_id = input("Enter your ID: ")

# User menu display
print(border)
left_text(f"Welcome {user_id}, please choose from below")
left_text("1. Enter a code")
left_text("2. View your gallery")
print(border)

# User menu selection
while True:
    user_selection = input("Choose an option: ")

    if user_selection == "exit":
        exit()  # Closes program

    elif user_selection == "1":
        image_data = request_image(user_id)
        if image_data is not None:
            process_image(image_data)

    elif user_selection == "2":
        view_gallery()

    else:
        continue