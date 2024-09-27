import pygame
from tkinter import filedialog
pygame.init()
pygame.font.init()


SIZE = 32
RES = (25*SIZE, 20*SIZE)
FPS = 60
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
PURPLE = [24, 20, 27]
FONT = pygame.font.SysFont('Comic Sans MS', SIZE//2)


class Button():
    def __init__(self, x, y, width, height, color, mouseOverColor, text, textColor, callback, display = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        self.color = color
        self.mouseOverColor = mouseOverColor
        self.text = text
        self.textColor = textColor

        self.callback = callback
        self.callbackResponse = None

        self.holding = False
        self.display = display
        
        self.mouseOver = False
    
    def draw(self, surf):
        if self.display:
            textW, textH = FONT.size(self.text)

            if textW > self.width:
                self.width = textW
            if textH > self.height:
                self.height = textH
            
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
            if self.mouseOver:
                pygame.draw.rect(surf, self.mouseOverColor, self.rect)
            else:
                pygame.draw.rect(surf, self.color, self.rect)

            surf.blit(FONT.render(self.text, True, self.textColor), (self.x, self.y))
    
    def update(self, mousePos, mouse):
        if self.display:
            if (mousePos[0] >= self.x and mousePos[0] <= self.x + self.width) and (mousePos[1] >= self.y and mousePos[1] <= self.y + self.height):
                self.mouseOver = True
                self.color = self.mouseOverColor
                self.textColor = WHITE
            else:
                self.mouseOver = False
                self.color = WHITE
                self.textColor = BLACK
            
            if self.mouseOver and mouse[0] and not self.holding:
                self.holding = True
                self.callbackResponse = self.callback()  
            
            if not mouse[0]:
                self.holding = False

def readFile(path):
    file = open(path, 'r', encoding='utf-16')
    data = file.readlines()

    for element in data:
        if element == '\n':
            data.remove(element)

    newRes = [int(i) for i in data[1].split(' ')]
    
    pixels = []
    for line in data[2:]:
        for pixel in line.split(' '):
            pixels.append(pixel.replace('\n', ''))


    pixels = [0 if i == '' else int(i) for i in pixels]
    return newRes, pixels

def displayFile(res, surf, pixels):
    i = 0
    for y in range(0, res[1]):
        for x in range (0, res[0]):
            rect = pygame.Rect(x * SIZE, y * SIZE, SIZE, SIZE)
            pygame.draw.rect(surf, WHITE if pixels[i] == 1 else BLACK, rect)
            i += 1


win = pygame.display.set_mode(RES)
pygame.display.set_caption('PBM Viewer')
clock = pygame.time.Clock()
fileInputBtn = Button(RES[0]/2 - SIZE*2, RES[1] - SIZE*2, SIZE*4, SIZE, WHITE, PURPLE, 'Escolha o arquivo', BLACK, filedialog.askopenfilename)
run = True
path = ''
tutorialTexts = [
    'Só upa o .pbm, do tipo P1, que a janela vai redimensionar para o tamanho especificado.',
    'Cada pixel no arquivo será representado na janela com 32 pixels de lado.',
    'Depois de carregar o arquivo, você pode apertar R para atualizar a imagem mostrada',
    'caso alguma alteração tenha sido feita no arquivo.',
    '',
    '',
    'Boa sorte ae',
    'jho___on',
    ':D'
]


while run:
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos() 

    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_r] and not fileInputBtn.display:
        newRes, pixels = readFile(fileInputBtn.callbackResponse)
        win = pygame.display.set_mode((newRes[0] * SIZE, newRes[1] * SIZE))
        displayFile(newRes, win, pixels)
    
    # UI Updates
    if fileInputBtn.display:
        win.fill(BLACK)

        yOffset = 0
        for phrase in tutorialTexts:
            textW, textH = FONT.size(phrase)
            render_ = FONT.render(phrase, True, WHITE)
            win.blit(render_, (RES[0]//2 - textW//2, 80 + yOffset))
            yOffset += textH + 5

    fileInputBtn.draw(win)
    fileInputBtn.update(mousePos, mouse)

    if fileInputBtn.callbackResponse and fileInputBtn.display:
        fileInputBtn.display = False
        newRes, pixels = readFile(fileInputBtn.callbackResponse)
        win = pygame.display.set_mode((newRes[0] * SIZE, newRes[1] * SIZE))
        displayFile(newRes, win, pixels)

    pygame.display.update()
    clock.tick(FPS)
        