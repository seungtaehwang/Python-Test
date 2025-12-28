
import tkinter as tk

def on_canvas_configure(event):
    """내부 프레임 크기가 변경될 때 캔버스의 스크롤 영역을 업데이트합니다."""
    canvas.configure(scrollregion=canvas.bbox("all"))

root = tk.Tk()
root.title("Scrollable Canvas with Multiple Canvases")

# 1. 메인 프레임 (컨테이너 역할)
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# 2. 캔버스 생성
canvas = tk.Canvas(main_frame, bg='white')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# 3. 스크롤바 생성 및 연결
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# 4. 캔버스 안에 들어갈 내부 프레임 생성
# 이 프레임 안에 실제 위젯들이 배치됩니다.
canvas_frame = tk.Frame(canvas, bg='lightgray')

# 5. create_window를 사용하여 내부 프레임을 캔버스에 추가
# anchor='nw'는 프레임의 북서쪽(top-left) 모서리를 캔버스의 좌표 (0, 0)에 고정합니다.
canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

# 6. 내부 프레임의 크기 변경 이벤트를 캔버스 스크롤 영역에 바인딩
canvas_frame.bind("<Configure>", on_canvas_configure)

# 7. 내부 프레임 안에 다수의 작은 캔버스 (또는 다른 위젯) 배치
for i in range(10):
    # 내부 프레임을 부모로 하는 새로운 작은 캔버스 생성
    small_canvas = tk.Canvas(canvas_frame, width=300, height=100, bg=f'#{i*10}{i*10}{i*10}', relief=tk.RAISED, borderwidth=2)
    small_canvas.pack(pady=10, padx=10)
    small_canvas.create_text(150, 50, text=f"Canvas {i+1}", font=("Helvetica", 16))

root.mainloop()