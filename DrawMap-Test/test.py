import tkinter as tk

def create_canvases(parent_frame):
    """
    주어진 부모 프레임 내에 여러 개의 캔버스 위젯을 생성하고 배치합니다.
    """
    for row in range(100):  # 3개의 행
        for col in range(3):  # 2개의 열
            # 각 캔버스 생성
            ss_canvas = tk.Canvas(parent_frame, width=300, height=300, bg='white', borderwidth=1)
            
            # 캔버스에 간단한 텍스트 추가 (식별용)
            ss_canvas.create_text(50, 50, text=f"Row {row}\nCol {col}")
            
            # grid 레이아웃 관리자를 사용하여 프레임 내에 배치
            # padx, pady로 간격 설정
            ss_canvas.grid(row=row, column=col, padx=2, pady=2)

def on_canvas_configure(event):
    """내부 프레임 크기가 변경될 때 캔버스의 스크롤 영역을 업데이트합니다."""
    canvas.configure(scrollregion=canvas.bbox("all"))


# 메인 윈도우 생성
root = tk.Tk()
root.title("다수의 Canvas 배치 예제")
root.geometry("953x630")

canvas = tk.Canvas(root, bg='white', scrollregion=(0, 0, 1000, 700))
scrollbar = tk.Scrollbar(root, command=canvas.yview)

# Configure the canvas to use the scrollbar and pack them
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



# 4. 캔버스 안에 들어갈 내부 프레임 생성
# 이 프레임 안에 실제 위젯들이 배치됩니다.
#canvas_frame = tk.Frame(canvas, bg='white')

# 5. create_window를 사용하여 내부 프레임을 캔버스에 추가
# anchor='nw'는 프레임의 북서쪽(top-left) 모서리를 캔버스의 좌표 (0, 0)에 고정합니다.
#canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

# 6. 내부 프레임의 크기 변경 이벤트를 캔버스 스크롤 영역에 바인딩
canvas.bind("<Configure>", on_canvas_configure)

# 함수 호출하여 프레임 내에 캔버스 배치
create_canvases(canvas)


# Set focus to the canvas so it receives the events immediately
canvas.focus_set()

# GUI 이벤트 루프 시작
root.mainloop()