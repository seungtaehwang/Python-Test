import tkinter as tk

def on_mousewheel(event):
    # Determine the scroll direction and amount based on the OS
    if event.num == 4 or event.delta > 0:
        # Scroll up (Linux Button-4 or Windows/macOS positive delta)
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        # Scroll down (Linux Button-5 or Windows/macOS negative delta)
        canvas.yview_scroll(1, "units")

root = tk.Tk()
root.geometry("400x300")

# Create a canvas and a scrollbar
canvas = tk.Canvas(root, bg='white', scrollregion=(0, 0, 500, 500))
scrollbar = tk.Scrollbar(root, command=canvas.yview)

# Configure the canvas to use the scrollbar and pack them
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Add some content to the canvas (e.g., a rectangle)
canvas.create_rectangle(10, 10, 400, 400, fill="lightblue")
canvas.create_text(250, 450, text="Scroll down to see this text")

# Bind mouse wheel events to the canvas
# Windows/macOS binding
canvas.bind("<MouseWheel>", on_mousewheel)
# Linux bindings (Button-4 for scroll up, Button-5 for scroll down)
canvas.bind("<Button-4>", on_mousewheel)
canvas.bind("<Button-5>", on_mousewheel)

# Set focus to the canvas so it receives the events immediately
canvas.focus_set()

root.mainloop()