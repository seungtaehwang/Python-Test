import tkinter as tk
import turtle
import math

# --- Configuration in micrometers (um) ---
WAFER_DIAMETER_UM = 200000 
DIE_SIZE_X_UM = 5096
DIE_SIZE_Y_UM = 4028
STREET_WIDTH_UM = 10 # Space between dies
EDGE_EXCLUSION_UM = 1500 # Margin from the edge

# --- Scaling Factor ---
# Define a scale: 1 pixel = 100 um for a reasonable screen size
SCALE_FACTOR = WAFER_DIAMETER_UM // 800.0
WAFER_DIAMETER_PX = WAFER_DIAMETER_UM // SCALE_FACTOR
DIE_SIZE_X_PX = DIE_SIZE_X_UM // SCALE_FACTOR
DIE_SIZE_Y_PX = DIE_SIZE_Y_UM // SCALE_FACTOR
STREET_WIDTH_PX = STREET_WIDTH_UM // SCALE_FACTOR
EDGE_EXCLUSION_PX = EDGE_EXCLUSION_UM // SCALE_FACTOR
TOP_LABLE_SPACE_PX = 30

# Calculate total step size for grid placement
STEP_X_PX = DIE_SIZE_X_PX + STREET_WIDTH_PX
STEP_Y_PX = DIE_SIZE_Y_PX + STREET_WIDTH_PX
WAFER_RADIUS_PX = WAFER_DIAMETER_PX // 2


def on_canvas_configure(event):
    """내부 프레임 크기가 변경될 때 캔버스의 스크롤 영역을 업데이트합니다."""
    canvas.configure(scrollregion=canvas.bbox("all"))

def create_map(parent_frame, col, row, mapsize):
    """
    주어진 부모 프레임 내에 여러 개의 캔버스 위젯을 생성하고 배치합니다.
    """
    # 각 캔버스 생성
    ss_canvas = tk.Canvas(parent_frame, width=mapsize+3, height=mapsize+60, bg='white', borderwidth=1)
    
    # grid 레이아웃 관리자를 사용하여 프레임 내에 배치
    # padx, pady로 간격 설정
    ss_canvas.grid(row=row, column=col, padx=1, pady=1)
    screen = turtle.TurtleScreen(ss_canvas)
    screen.tracer(0)
    map = turtle.RawTurtle(screen)

    draw_wafer_map(map, col, row, mapsize)
    screen.update() 

def draw_wafer_map(map, col, row, mapsize):
    map.speed(0)
    map.hideturtle()

    global SCALE_FACTOR, WAFER_DIAMETER_PX, DIE_SIZE_X_PX, DIE_SIZE_Y_PX, STREET_WIDTH_PX, EDGE_EXCLUSION_PX
    
    SCALE_FACTOR = WAFER_DIAMETER_UM // mapsize
    WAFER_DIAMETER_PX = WAFER_DIAMETER_UM // SCALE_FACTOR
    DIE_SIZE_X_PX = DIE_SIZE_X_UM // SCALE_FACTOR
    DIE_SIZE_Y_PX = DIE_SIZE_Y_UM // SCALE_FACTOR
    STREET_WIDTH_PX = STREET_WIDTH_UM // SCALE_FACTOR
    EDGE_EXCLUSION_PX = EDGE_EXCLUSION_UM // SCALE_FACTOR

    # Calculate total step size for grid placement
    global STEP_X_PX, STEP_Y_PX, WAFER_RADIUS_PX
    
    STEP_X_PX = DIE_SIZE_X_PX + STREET_WIDTH_PX
    STEP_Y_PX = DIE_SIZE_Y_PX + STREET_WIDTH_PX
    WAFER_RADIUS_PX = WAFER_DIAMETER_PX // 2

    # Draw the outer wafer boundary
    draw_circle(map, WAFER_RADIUS_PX, 0, 0, color="gray")

    # Draw the edge exclusion boundary
    #draw_circle(map, WAFER_RADIUS_PX - EDGE_EXCLUSION_PX, 0, 0, color="red")

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
                #print(die_x, die_y)
                draw_die(map, die_x, die_y, DIE_SIZE_X_PX, DIE_SIZE_Y_PX, "lightgray")
            
    # Add a title in actual units for clarity
    map.goto(0, WAFER_RADIUS_PX + 30 - TOP_LABLE_SPACE_PX)
    map.write(f"Wafer Map (Diameter: {WAFER_DIAMETER_UM/1000:.0f} mm) [{col}, {row}]", align="center", font=("Arial", 12, "bold"))
    map.goto(0, WAFER_RADIUS_PX + 10 - TOP_LABLE_SPACE_PX)
    map.write(f"Die size: {DIE_SIZE_X_UM}x{DIE_SIZE_Y_UM} um (Scale: 1px = {SCALE_FACTOR}um)", align="center", font=("Arial", 9, "normal"))

def draw_circle(map, radius, x, y, color="gray"):
    """Helper function to draw a circle at a specific coordinate."""
    map.penup()
    map.goto(x, y - radius - TOP_LABLE_SPACE_PX)
    map.pendown()
    map.color(color)
    map.circle(radius)
    map.penup()

def draw_die(map, x, y, width, height, fill_color="lightgray", border_color="gray"):
    """Helper function to draw a single die (rectangle) at a specific coordinate."""
    map.penup()
    map.goto(x, y- TOP_LABLE_SPACE_PX)
    map.pendown()
    map.color(border_color, fill_color)
    map.begin_fill()
    for _ in range(2):
        map.forward(width)
        map.left(90)
        map.forward(height)
        map.left(90)
    map.end_fill()
    map.penup()

def is_within_wafer(x, y, width, height, radius):
    """Check if a coordinate is within the circular wafer boundary."""
    # Wafer center is assumed at (0, 0)
    valid = False

    if x < 0 and y < 0:
        # Bottom-left corner
        valid = math.sqrt(x**2 + y**2) <= radius

    if x < 0 and y >= 0:
        # Bottom-left corner
        valid = math.sqrt(x**2 + (y+DIE_SIZE_Y_PX)**2) <= radius

    if x >= 0 and y >= 0:
        # Bottom-left corner
        valid = math.sqrt((x+DIE_SIZE_X_PX)**2 + (y+DIE_SIZE_Y_PX)**2) <= radius

    if x >= 0 and y < 0:
        # Bottom-left corner
        valid = math.sqrt((x+DIE_SIZE_X_PX)**2 + (y)**2) <= radius

    return valid


# 1. 메인 윈도우 생성
root = tk.Tk()
root.title("Wafer Map Gallery Viewer")
root.geometry("1240x900")

top_frame = tk.Frame(root, height=50, bg='lightgray')
top_frame.pack(side=tk.TOP, fill=tk.X)  
row_label = tk.Label(top_frame, text="Rows :", bg='lightgray', font=("Arial", 10))
row_label.pack(side=tk.LEFT, fill=tk.X, padx=10)
row_entry = tk.Entry(top_frame, width=5, font=("Arial", 10), text ="5")
row_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
col_label = tk.Label(top_frame, text="Columns :", bg='lightgray', font=("Arial", 10))
col_label.pack(side=tk.LEFT, fill=tk.X, padx=10) 
col_entry = tk.Entry(top_frame, width=5, font=("Arial", 10), text ="2")
col_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
draw_button = tk.Button(top_frame, text="Draw Map", font=("Arial", 10), command=lambda: draw())
draw_button.pack(side=tk.LEFT, fill=tk.X, padx=10)
# 2. Configure the canvas to use the scrollbar and pack them
canvas = tk.Canvas(root, bg='white', scrollregion=(0, 0, 1000, 700))
scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)            
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 3. 캔버스 안에 들어갈 내부 프레임 생성
# 이 프레임 안에 실제 위젯들이 배치됩니다. 
# 4. create_window를 사용하여 내부 프레임을 캔버스에 추가
# anchor='nw'는 프레임의 북서쪽(top-left) 모서리를 캔버스의 좌표 (0, 0)에 고정합니다.
# 5. 내부 프레임의 크기 변경 이벤트를 캔버스 스크롤 영역에 바인딩
canvas_frame = tk.Frame(canvas, bg='white')
canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
canvas_frame.bind("<Configure>", on_canvas_configure)


# 6. 함수 호출하여 프레임 내에 캔버스(map) 배치
def draw():
    # Clear previous widgets in the frame
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    width = canvas.winfo_width()- 40   
    map_size = width / int(col_entry.get())
    for row in range(int(row_entry.get())):  # 5개의 열
        for col in range(int(col_entry.get())):  # 2개의 행
            create_map(canvas_frame, col, row, int(map_size))

root.mainloop()