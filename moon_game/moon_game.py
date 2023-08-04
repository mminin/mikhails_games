import matplotlib.pyplot as plt
import random
from PIL import Image
# Load the image
moon_image_path = "assets/moon_unannotized.png"
moon_image = Image.open(moon_image_path)
# Define the regions (rough approximation for now)
regions = {
    "Mare Imbrium": [120, 210, 60, 120],
    "Oceanus Procellarum": [40, 100, 100, 210],
    "Mare Serenitatis": [220, 280, 90, 140],
    "Mare Tranquillitatis": [280, 330, 160, 190],
    "Mare Fecunditatis": [340, 360, 200, 245],
    "Mare Crisium": [350, 380, 120, 160],
    "Mare Nectaris": [290, 320, 240, 260],
    "Mare Frigoris": [150, 300, 25, 40],
    "Mare Humorum": [80, 100, 260, 290],
    "Mare Nubium": [130, 180, 250, 290],
    "Mare Moscoviense": [490, 520, 95, 120]
}
def plot_random_asterisk(mare_name):
    plt.figure(figsize=(14, 10))
    """Plot an asterisk at a random point within a given mare."""
    # Get the region of the mare
    x_min, x_max, y_min, y_max = regions[mare_name]   
    # Generate a random point within this region
    x = random.randint(x_min, x_max)
    y = random.randint(y_min, y_max)
    # Plot the image and the asterisk
    plt.imshow(moon_image)
    plt.scatter(x, y, c='r', marker='*')
    plt.show()
# Test the function with a random mare
plot_random_asterisk("Mare Moscoviense")



import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
import random
from PIL import Image
# Load the image
moon_image_path = "assets/moon_unannotized.png"
moon_image = Image.open(moon_image_path)
# Define the regions (rough approximation for now)
regions = {
    "Mare Imbrium": [120, 210, 60, 120],
    "Oceanus Procellarum": [40, 100, 100, 210],
    "Mare Serenitatis": [220, 280, 90, 140],
    "Mare Tranquillitatis": [280, 330, 160, 190],
#    "Mare Fecunditatis": [340, 360, 200, 245],
#    "Mare Crisium": [350, 380, 120, 160],
#    "Mare Nectaris": [290, 320, 240, 260],
#    "Mare Frigoris": [150, 300, 25, 40],
#    "Mare Humorum": [80, 100, 260, 290],
#    "Mare Nubium": [130, 180, 250, 290],
#    "Mare Moscoviense": [490, 520, 95, 120]
}
# Create the main window
window = tk.Tk()

# Create a global variable to store the PhotoImage
global moon_photo

# Create a PhotoImage object from the PIL Image
moon_photo = ImageTk.PhotoImage(moon_image)

# Create a label for the counter
counter_label = tk.Label(window)
counter_label.grid(row=0, column=0, sticky='w')  # Place it at the top left

# Create a canvas for the image
canvas = tk.Canvas(window, width=moon_image.width, height=moon_image.height)
canvas.grid(row=1, column=0, columnspan=4)  # Place it below the label and let it span all columns

# Create a frame for the buttons
button_frame = tk.Frame(window)
button_frame.grid(row=2, column=0, columnspan=4)  # Place it below the canvas and let it span all columns

# Create the buttons
buttons = []
button_colors = []
for i in range(4):
    button = tk.Button(button_frame, command=lambda i=i: check_guess(i))
    button.pack(side='left')
    buttons.append(button)
    button_colors.append(button.cget('background'))  # Save the initial button color


def get_random_mare_and_point():
    """Choose a random mare and a random point within it."""
    mare_name = random.choice(list(regions.keys()))
    x_min, x_max, y_min, y_max = regions[mare_name]
    x = random.randint(x_min, x_max)
    y = random.randint(y_min, y_max)
    return mare_name, x, y

def start_new_round():
    """Start a new round of the game."""
    global correct_mare
    correct_mare, x, y = get_random_mare_and_point()
    # If there are no more mares, don't start a new round
    if correct_mare is None:
        return
    
    # Clear the canvas
    canvas.delete('all')

    # Add the image to the canvas
    canvas.create_image(0, 0, image=moon_photo, anchor='nw')

    # Add a small oval (the point) to the canvas
    radius = 5
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red')

    # Reset button colors
    for button, color in zip(buttons, button_colors):
        button.config(bg=color)

    # Update the buttons
    update_buttons()

def update_buttons():
    """Update the labels on the buttons with new guesses."""
    # Randomly choose the correct button
    correct_button_index = random.randint(0, 3)
    
    # Create a list of other mares, excluding the correct one
    other_mares = [mare for mare in regions.keys() if mare != correct_mare]
    random.shuffle(other_mares)
    
    # Set the text for each button
    for i in range(4):
        if i == correct_button_index:
            buttons[i].config(text=correct_mare, state='normal')
        elif i < len(other_mares):
            buttons[i].config(text=other_mares[i], state='normal')
        else:
            buttons[i].config(text='', state='disabled')

def blink(button, color1, color2, times_left):
    """Change the color of the button, then schedule the next color change."""
    if times_left > 0:
        if button.cget('bg') == color1:
            button.config(bg=color2)
            window.after(100, lambda: blink(button, color1, color2, times_left - 1))
        else:
            button.config(bg=color1)
            window.after(100, lambda: blink(button, color1, color2, times_left - 1))
    else:
        # If no more blinks left, start a new round after 100ms
        window.after(100, start_new_round)

# Initialize the counters
counters = {mare: 10 for mare in regions}

def check_guess(i):
    """Check whether the guess was correct and show feedback."""
    global correct_mare
    button = buttons[i]
    if button.cget('text') == correct_mare:
        button.config(bg='green')
        # Decrement the counter for the correct mare
        counters[correct_mare] -= 1
        # If the counter for the correct mare reaches 0, remove it from the regions and counters
        if counters[correct_mare] == 0:
            del regions[correct_mare]
            del counters[correct_mare]
        # Start a new round after 100ms
        window.after(100, start_new_round)
    else:
        button.config(bg='red')
        # Increment the counter for the correct mare, but not above 10
        counters[correct_mare] = min(10, counters[correct_mare] + 1)
        # Find the correct button and make it blink
        for button in buttons:
            if button.cget('text') == correct_mare:
                blink(button, 'green', 'red', 5)
                break
    # Update the counter label
    if counters:
        max_counter = max(counters.values())
    else:
        max_counter = 0
    counter_label.config(text=f"Largest counter: {max_counter}")


def get_random_mare_and_point():
    """Choose a random mare and a random point within it."""
    if not regions:
        messagebox.showinfo("Congratulations!", "YOU WIN!")
        return None, None, None
    mare_name = random.choice(list(regions.keys()))
    x_min, x_max, y_min, y_max = regions[mare_name]
    x = random.randint(x_min, x_max)
    y = random.randint(y_min, y_max)
    return mare_name, x, y

# Start the first round
start_new_round()

# Start the main loop
window.mainloop()

# Update the counter label
if counters:
    max_counter = max(counters.values())
else:
    max_counter = 0
counter_label.config(text=f"Largest counter: {max_counter}")
