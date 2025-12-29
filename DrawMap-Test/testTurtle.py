
import tkinter as tk
import turtle

# 1. 메인 Tkinter 윈도우 생성
root = tk.Tk()
root.title("여러 마리 터틀 예제")

# 2. Tkinter 캔버스 위젯 생성
canvas = tk.Canvas(master=root, width=600, height=400, bg="white")
canvas.pack()

# 3. 캔버스를 터틀 스크린으로 설정
screen = turtle.TurtleScreen(canvas)

# 4. 여러 개의 RawTurtle 객체 생성 및 설정
# RawTurtle은 Tkinter 캔버스 위에서 작동하는 터틀 객체입니다.
turtles = []  # 터틀 객체들을 저장할 리스트

for i in range(5):
    t = turtle.RawTurtle(screen)
    t.shape("turtle")
    t.speed(0)  # 속도 설정
    t.hideturtle()  # 터틀 숨기기
    t.penup()   # 펜 들기
    
    # 각 터틀의 초기 위치 및 색상 설정
    if i % 2 == 0:
        t.color("red")
        t.goto(-200 + i * 100, 50)
    else:
        t.color("blue")
        t.goto(-200 + i * 100, -50)
        
    t.pendown() # 펜 내리기
    turtles.append(t)

# 5. 각 터틀에게 명령 실행 (예시: 앞으로 이동)
for t in turtles:
    t.forward(100)
    t.left(90)

# Tkinter 이벤트 루프 시작
root.mainloop()