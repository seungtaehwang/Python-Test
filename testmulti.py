import tkinter as tk
import turtle
import random

def create_wafer_window(parent_root, title, wafer_data):
    """
    Tkinter Toplevel 창, Canvas, TurtleScreen, RawTurtle을 생성합니다.
    """
    window = tk.Toplevel(parent_root)
    window.title(title)
    canvas = tk.Canvas(window, width=300, height=300, bg="white")
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    t = turtle.RawTurtle(screen)
    t.speed(0) # 그리기 속도 최대로 설정
    
    # 웨이퍼 맵 데이터 그리기 (예시 함수)
    draw_wafer_map(t, wafer_data)
    
    return window, t

def draw_wafer_map(a_turtle, data):
    """
    주어진 RawTurtle 객체를 사용하여 웨이퍼 맵을 그립니다.
    """
    a_turtle.penup()
    # 데이터를 기반으로 웨이퍼 맵의 다이(die)를 그리는 로직 구현
    # 예시: 랜덤한 위치에 점 찍기
    for _ in range(50):
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        color = random.choice(["red", "green", "blue", "black"])
        a_turtle.goto(x, y)
        a_turtle.dot(5, color) # 5 크기의 점 그리기

def main():
    root = tk.Tk()
    root.withdraw() # 메인 Tkinter 창을 숨김

    # 각기 다른 웨이퍼 데이터 준비 (예시 데이터)
    wafer_data_1 = [...] 
    wafer_data_2 = [...]
    wafer_data_3 = [...]

    # 여러 개의 독립적인 창 생성
    win1, t1 = create_wafer_window(root, "Wafer 1 Map", wafer_data_1)
    win2, t2 = create_wafer_window(root, "Wafer 2 Map", wafer_data_2)
    win3, t3 = create_wafer_window(root, "Wafer 3 Map", wafer_data_3)
    
    # Tkinter 이벤트 루프 시작
    # 이 루프가 실행되는 동안 모든 창이 활성 상태로 유지됩니다.
    tk.mainloop()

if __name__ == "__main__":
    main()