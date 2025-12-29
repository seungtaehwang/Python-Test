import tkinter as tk
import turtle as t
import math

# --- Configuration in micrometers (um) ---
WAFER_DIAMETER_UM = 150000 
DIE_SIZE_X_UM = 5096
DIE_SIZE_Y_UM = 4028
STREET_WIDTH_UM = 50 # Space between dies
EDGE_EXCLUSION_UM = 2000 # Margin from the edge

# --- Scaling Factor ---
# Define a scale: 1 pixel = 100 um for a reasonable screen size
SCALE_FACTOR = WAFER_DIAMETER_UM // 800.0
WAFER_DIAMETER_PX = WAFER_DIAMETER_UM // SCALE_FACTOR
DIE_SIZE_X_PX = DIE_SIZE_X_UM // SCALE_FACTOR
DIE_SIZE_Y_PX = DIE_SIZE_Y_UM // SCALE_FACTOR
STREET_WIDTH_PX = STREET_WIDTH_UM // SCALE_FACTOR
EDGE_EXCLUSION_PX = EDGE_EXCLUSION_UM // SCALE_FACTOR

# Calculate total step size for grid placement
STEP_X_PX = DIE_SIZE_X_PX + STREET_WIDTH_PX
STEP_Y_PX = DIE_SIZE_Y_PX + STREET_WIDTH_PX
WAFER_RADIUS_PX = WAFER_DIAMETER_PX // 2

# --- Turtle Setup ---

t.setup(width=830, height=890)
t.speed(0) # Fastest drawing speed
t.hideturtle()
t.tracer(0, 0) # Turn off automatic animation for faster drawing

def draw_circle(radius, x, y, color="gray"):
    """Helper function to draw a circle at a specific coordinate."""
    t.penup()
    t.goto(x, y - radius -30)
    t.pendown()
    t.color(color)
    t.circle(radius)
    t.penup()

def draw_die(x, y, width, height, fill_color="lightgray", border_color="gray"):
    """Helper function to draw a single die (rectangle) at a specific coordinate."""
    t.penup()
    t.goto(x, y-30)
    t.pendown()
    t.color(border_color, fill_color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()
    t.penup()

def is_within_wafer(x, y, width, height, radius):
    """Check if a coordinate is within the circular wafer boundary."""
    # Wafer center is assumed at (0, 0)
    valid = False

    if x < 0 and y < 0:
        # Bottom-left corner
        valid = math.sqrt(x**2 + y**2) <= radius

    if x < 0 and y > 0:
        # Bottom-left corner
        valid = math.sqrt(x**2 + (y+DIE_SIZE_Y_PX)**2) <= radius

    if x > 0 and y > 0:
        # Bottom-left corner
        valid = math.sqrt((x+DIE_SIZE_X_PX)**2 + (y+DIE_SIZE_Y_PX)**2) <= radius

    if x > 0 and y < 0:
        # Bottom-left corner
        valid = math.sqrt((x+DIE_SIZE_X_PX)**2 + (y)**2) <= radius

    return valid

def create_wafer_map():
    # Draw the outer wafer boundary
    draw_circle( WAFER_RADIUS_PX, 0, 0, color="gray")

    # Draw the edge exclusion boundary
    #draw_circle(WAFER_RADIUS_PX - EDGE_EXCLUSION_PX, 0, 0, color="red")

    # Calculate grid range for dies
    # Start the grid from the bottom-left corner of the potential die area
    start_x = -WAFER_RADIUS_PX
    start_y = -WAFER_RADIUS_PX

    # Iterate through possible die positions in a grid
    for i in range(int(WAFER_DIAMETER_PX / STEP_X_PX) + 1):
        for j in range(int(WAFER_DIAMETER_PX / STEP_Y_PX) + 1):
            # Calculate die position based on grid index
            die_x = start_x + i * STEP_X_PX
            die_y = start_y + j * STEP_Y_PX

            # Check if the die's center is within the wafer's radius
            # We check the center for simplicity in this example
            if is_within_wafer(die_x, die_y, DIE_SIZE_X_PX, DIE_SIZE_Y_PX, WAFER_RADIUS_PX - EDGE_EXCLUSION_PX):
                # Apply bin code logic here (e.g., color based on pass/fail data)
                # For this example, all inner dies are colored blue
                draw_die(die_x, die_y, DIE_SIZE_X_PX, DIE_SIZE_Y_PX, "lightgray")
            
    # Add a title in actual units for clarity
    t.goto(0, WAFER_RADIUS_PX + 30 -30)
    t.write(f"Wafer Map (Diameter: {WAFER_DIAMETER_UM/1000:.0f} mm)", align="center", font=("Arial", 16, "bold"))
    t.goto(0, WAFER_RADIUS_PX + 10-30)
    t.write(f"Die size: {DIE_SIZE_X_UM}x{DIE_SIZE_Y_UM} um (Scale: 1px = {SCALE_FACTOR}um)", align="center", font=("Arial", 10, "normal"))


# --- Main execution ---
create_wafer_map()
t.update() # Update the screen after all drawing is done
t.mainloop() # Keep the window open