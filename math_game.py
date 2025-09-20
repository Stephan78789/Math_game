
from pygame import *
from random import *
import sys

window = display.set_mode((1200,900))
display.set_caption('Math_game')

WIDTH, HEIGHT = 1200, 900
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CIRCLE_RADIUS = 30

font.init()
font1 = font.SysFont('arial', 36)
font2 = font.SysFont('arial', 44)

class Button():
    def __init__(self, x,y,weight,height, color):
        self.rect = Rect(x,y,weight,height)
        self.fill_color = color

    def set_text(self, text, color, font_size):
        self.image = font.SysFont('arial',font_size).render(text,1,color)

    def reset(self,shift_x,shift_y):
        draw.rect(window, self.fill_color, self.rect)
        window.blit(self.image,(self.rect.x + shift_x,self.rect.y + shift_y))

    def click_mouse(self,x,y):
        return self.rect.collidepoint(x,y)

class Circle():

    def __init__(self, x, y , answer):
        self.x = x
        self.y = 0
        self. answer = answer
        self.color = GREEN

    def fall(self):
        self.y +=3
        #if self.y > HEIGHT:
            #self.y = 0
    def draw(self,surface):
        draw.circle(surface,self.color, (self.x, self.y), CIRCLE_RADIUS)
        text =font1.render(str(self.answer), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text,text_rect)

    
    
def generate_question():
    num1 = randint(1,10)
    num2 = randint(1,10)
    question = str(num1) + ' + ' + str(num2) + ' = '
    answer = num1 + num2
    return question, answer

circles = []

def generate_circles():
    question, correct_answer = generate_question()
    pos_circles = [[0,285],[315,585],[615, 885],[915,1200]]
    shuffle(pos_circles)
    for i in range(4):
        if i == 0:
            circle = Circle(randint(pos_circles[i][0],pos_circles[i][1]),0,correct_answer)
        else:
            circle = Circle(randint(pos_circles[i][0],pos_circles[i][1]),0,randint(2,50))
        circles.append(circle)
    return question, correct_answer
    
question, correct_answer = generate_circles()
    

clock =time.Clock()
score = 0
max_score = 10
FPS = 60
game = True
finish = True
click = False
menu = True
btn_restart = Button(470,500,200,70,(0,255,0))
btn_restart.set_text('Начать заново',(0,0,0), 33)
btn_start = Button(510,400,150,70,(0,255,0))
btn_start.set_text('Старт',(0,0,0), 40)

while game:
    window.fill(WHITE)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = mouse.get_pos()
            if btn_start.click_mouse(mouse_x,mouse_y) and  menu:
                menu = False
                finish = False
                score = 0
            if btn_restart.click_mouse(mouse_x,mouse_y) and finish:
                finish = False
                score = 0
            for circle in circles:
                if (circle.x - CIRCLE_RADIUS <= mouse_x <= circle.x + CIRCLE_RADIUS) and (circle.y - CIRCLE_RADIUS <= mouse_y <= circle.y + CIRCLE_RADIUS):
                    if circle.answer == correct_answer:
                        score +=1 
                    else:
                        score -=1
                        if score < 0:
                            score = 0 
                    circles.remove(circle)
                    click = True
    if score >= max_score:
        win_text = font2.render('Вы выиграли!', True, (0, 255, 0))
        window.blit(win_text,(450,400))
        finish = True
        btn_restart.reset(10, 10)
    if menu:
        score = 0
        btn_start.reset(30,10)
    if not finish and not menu:
        if circles[0].y > HEIGHT or click:
            click = False
            circles = list()
            question, correct_answer= generate_circles()



        for s in circles:
            s.draw(window)
            s.fall()


    
        score_text = font1.render('Счёт: ' + str(score), True, (0, 0, 0))
        question_text = font1.render(question, True, (0, 0, 0))
        window.blit(score_text, (15,15))
        window.blit(question_text,(550,15))

    clock.tick(FPS)
    display.update()
    

