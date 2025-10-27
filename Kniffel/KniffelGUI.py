#---------------------------------------------
# Dateiname: KniffelGUI.py
# Darstellung des Spielfensters mit pygame
# Autor: Alex Stiller
# Letzte Änderung: 27.10.2025
#---------------------------------------------
import pygame
from random import randint
from KniffelGameLogic import DiceState

IMAGE_PATH = "Kniffel/Bilder"

class UIHelper:
    def __init__(self, screen, diceSize):
        self.screen = screen
        self.diceImg = []
        self.diceImg.append(pygame.image.load(f"{IMAGE_PATH}/wuerfelbild 1.png").convert_alpha())
        self.diceImg.append(pygame.image.load(f"{IMAGE_PATH}/wuerfelbild 2.png").convert_alpha())
        self.diceImg.append(pygame.image.load(f"{IMAGE_PATH}/wuerfelbild 3.png").convert_alpha())
        self.diceImg.append(pygame.image.load(f"{IMAGE_PATH}/wuerfelbild 4.png").convert_alpha())
        self.diceImg.append(pygame.image.load(f"{IMAGE_PATH}/wuerfelbild 5.png").convert_alpha())
        self.diceImg.append(pygame.image.load(f"{IMAGE_PATH}/wuerfelbild 6.png").convert_alpha())
        
        self.diceSize = diceSize
        self.diceSizeBig = diceSize*2
        
        self.textColor = (100,100,100)
        self.colorDarkRed = (200,100,100)
        fontSizeText = 40
        fontSizeEntry = 64
        
        self.font = pygame.font.SysFont(None, fontSizeEntry)
        self.fontText = pygame.font.SysFont(None, fontSizeText)
        
    def getDiceImage(self, diceValue, isBig = False):
        if isBig:
            return pygame.transform.scale(self.diceImg[diceValue], (self.diceSizeBig, self.diceSizeBig))    
        return pygame.transform.scale(self.diceImg[diceValue], (self.diceSize,self.diceSize))
    
    def getDiceImageWithScale(self, diceValue, scale):
        return pygame.transform.scale(self.diceImg[diceValue], (self.diceSize*scale,self.diceSize*scale))
    
    def getFontInst(self, text, isBig=True):
        if isBig:
            return self.font.render(text, True, self.textColor)
        else:
            return self.fontText.render(text, True, self.textColor)
        
    def getRedFontInst(self, text):
        return self.font.render(text, True, self.colorDarkRed)
        
    def blit(self, obj, pos):
        return self.screen.blit(obj, pos)
    
class KniffelGUI:
    def __init__(self, screenSize):
        self.screen = pygame.display.set_mode(screenSize)
        self.screenSize = screenSize
                 
        self.background = pygame.image.load(f"{IMAGE_PATH}/back.jpg").convert()    
        
        self.scoreTop = 0
        self.scoreBottom = 0
        self.scoreBonus = 0

        diceSize = 40
        self.uiHelper = UIHelper(self.screen, diceSize)
        
        self.shaker = ShakerUi()
        
        self.loadButton = Button(f"{IMAGE_PATH}/download.png", (40,40), (screenSize[0] - 60, screenSize[1] - 60))
        self.saveButton = Button(f"{IMAGE_PATH}/save.png", (40,40), (screenSize[0] - 110, screenSize[1] - 60))
        
        spaceStart = 10
        spaceText = 70
        spaceNextLine = 10
        startRow = 50
        rowSpace = 10
        line = 20
        ruleId = 0
        
        self.entries = []
        self.resultPosX = spaceText+ 3*self.uiHelper.diceSize
        for i in range(6):
            posRes = (self.resultPosX, line)
            posCat = (spaceStart, line)
            self.entries.append(EntryUi(ruleId, posCat, posRes))
            line += diceSize + spaceNextLine
            ruleId += 1
        
        self.posUpperTotal = (spaceStart, line)
        line += diceSize + spaceNextLine
        self.posBonus = (spaceStart, line)
        line += diceSize + spaceNextLine
        
        posRes = (self.resultPosX, line)
        posCat = (spaceStart, line)
        self.entries.append( EntryUiPasch(ruleId, posCat, posRes, 2))
        ruleId += 1
        line += diceSize + spaceNextLine
        
        posRes = (self.resultPosX, line)
        posCat = (spaceStart, line)
        self.entries.append( EntryUiPasch(ruleId, posCat, posRes, 3))
        ruleId += 1
        line += diceSize + spaceNextLine
        
        posRes = (self.resultPosX, line)
        posCat = (spaceStart, line)
        self.entries.append( EntryUiFullHouse(ruleId, posCat, posRes))
        ruleId += 1
        line += diceSize + spaceNextLine
        
        self.entries.append( EntryUiStreet(ruleId, (spaceStart, line), (self.resultPosX, line), 4))
        ruleId += 1
        line += diceSize + spaceNextLine
        
        self.entries.append( EntryUiStreet(ruleId, (spaceStart, line), (self.resultPosX, line), 5))
        ruleId += 1
        line += diceSize + spaceNextLine
        
        self.entries.append( EntryUiKniffel(ruleId, (spaceStart, line), (self.resultPosX, line)))
        ruleId += 1
        line += diceSize + spaceNextLine
        
        self.entries.append( EntryUiChance(ruleId, (spaceStart, line), (self.resultPosX, line)))
        line += diceSize + spaceNextLine
        
        self.posTotal = (spaceStart, line)
        
        self.diceObj = []
        for i in range(5):
            pos = (300, startRow)
            self.diceObj.append( DiceUi(i, pos))
            startRow += self.uiHelper.diceSizeBig+rowSpace       
        

    def create(self, isShaking):
        # clear screen
        self.screen.fill((125,125,125))
        
        self.drawField(isShaking)
    
    def refresh(self):
        # refresh screen
        pygame.display.flip()
    
    def updateValues(self, gameLogic):
        self.updateDices(gameLogic)
            
        for e in self.entries:
            e.update(gameLogic)
            
        self.scoreTop = gameLogic.getTopScore()
        self.scoreBottom = gameLogic.getBottomScore()
        self.scoreBonus = gameLogic.getBonusScore()
    
    def updateDices(self, gameLogic):
        for d in self.diceObj:
            d.update(gameLogic)
            
    def playerScored(self, gameLogic):
        self.updateValues(gameLogic)
        
    def drawField(self, isAnimating):
        bg = pygame.transform.rotate(self.background, 90)
        bg = pygame.transform.scale(bg, self.screenSize)
        self.screen.blit(bg,(0,0))
    
        # show block
        for e in self.entries:
            e.showCategory(self.uiHelper)
            e.showResult(self.uiHelper)
            
        self.createLine("Gesamt: ", self.posUpperTotal, str(self.scoreTop), (self.resultPosX, self.posUpperTotal[1]))
        result = str(self.scoreBonus)
        self.createLine("Bonus (63):", self.posBonus, result, (self.resultPosX, self.posBonus[1]))
        result = str(self.scoreTop + self.scoreBottom + self.scoreBonus)
        self.createLine("Total:", self.posTotal, result, (self.resultPosX, self.posTotal[1]))
        
        for d in self.diceObj:
            d.show(isAnimating, self.uiHelper)
        
        self.shaker.show(isAnimating, self.screen)
        self.loadButton.show(self.screen)
        self.saveButton.show(self.screen)
        
    def createLine(self, text, textPos, value, valuePos):
        text = self.uiHelper.getFontInst(text, False)
        self.uiHelper.blit(text, textPos)
        text = self.uiHelper.getFontInst(value, False)
        self.uiHelper.blit(text, valuePos)


class EntryUi:
    def __init__(self, ruleId, posCat, posRes):
        self.ruleId = ruleId
        self.positionCategory = posCat
        self.positionResult = posRes
        self.result = "0";
        self.clickRect = ()
        self.hasValue = False
    
    def update(self, gameLogic):
        self.result = str(gameLogic.getResultOfRule(self.ruleId))
        self.hasValue = not gameLogic.canScore(self.ruleId)
        
    def showCategory(self, helper:UIHelper):
        dice = helper.getDiceImage(self.ruleId)
        helper.blit(dice, self.positionCategory)
        helper.blit(dice, (self.positionCategory[0] + helper.diceSize + 5, self.positionCategory[1]))
        helper.blit(dice, (self.positionCategory[0] + 2*helper.diceSize + 10, self.positionCategory[1]))
        
    def showResult(self, helper:UIHelper):
        if self.hasValue:
            text = helper.getFontInst(self.result)
        else:
            text = helper.getRedFontInst(self.result)
        self.clickRect = helper.blit(text, self.positionResult)
        
    def isClicked(self, pos):
        return self.clickRect.collidepoint(pos)

class EntryUiPasch(EntryUi):
    def __init__(self, ruleId, posCat, posRes, dice):
        EntryUi.__init__(self, ruleId, posCat, posRes)
        self.dice = dice
        
    def showCategory(self, helper:UIHelper):
        dice = helper.getDiceImage(self.dice)
        helper.blit(dice, self.positionCategory)
        text = helper.getFontInst("'er", False)
        helper.blit(text, (20+helper.diceSize, self.positionCategory[1]))

class EntryUiFullHouse(EntryUi):
    def showCategory(self, helper:UIHelper):
        dings = self.positionCategory[0]
        for _ in range(2):
            dice = helper.getDiceImageWithScale(1, 0.65)
            helper.blit(dice, (dings, self.positionCategory[1]))
            dings += helper.diceSize*0.7
        for _ in range(3):
            dice = helper.getDiceImageWithScale(2, 0.65)
            helper.blit(dice, (dings, self.positionCategory[1]))
            dings += helper.diceSize*0.7

class EntryUiStreet(EntryUi):
    def __init__(self, ruleId, posCat, posRes, size):
        EntryUi.__init__(self, ruleId, posCat, posRes)
        self.size = size
        self.scale = 0.85
        if size == 5:
            self.scale = 0.65
        
    def showCategory(self, helper:UIHelper):
        for i in range(self.size):
            smallValue = helper.diceSize*self.scale
            dice = helper.getDiceImageWithScale(1+i, self.scale)
            helper.blit(dice, (self.positionCategory[0]+ (i*(smallValue+2)), self.positionCategory[1]))

class EntryUiKniffel(EntryUi):
    def showCategory(self, helper:UIHelper):
        for i in range(5):
            smallValue = helper.diceSize*0.65
            dice = helper.getDiceImageWithScale(4, 0.65)
            helper.blit(dice, (self.positionCategory[0]+ (i*(smallValue+2)), self.positionCategory[1]))

class EntryUiChance(EntryUi):
    def showCategory(self, helper:UIHelper):
        text = helper.getFontInst("Chance :", False)
        helper.blit(text, self.positionCategory)

class ShakerUi:
    def __init__(self):
        self.shaker = pygame.image.load(f"{IMAGE_PATH}/Becher.png").convert_alpha()
        self.shakerRotation = 0
        self.direction = 3
        self.shakerRect = 0
        
    def show(self, isAnimating, screen):
        startRow = 600
        cup = pygame.transform.scale(self.shaker, (100,100))
        if isAnimating:
            self.shakerRotation += self.direction;
            if abs(self.shakerRotation) >= 10:
                self.direction *= -1
            cup = pygame.transform.rotate(cup,self.shakerRotation)
        
        self.shakerRect = screen.blit(cup,  (280, startRow))
    
    def isClicked(self, pos):
        return self.shakerRect.collidepoint(pos)

class Button:
    def __init__(self, fileName, size, pos):
        self.image = pygame.image.load(fileName).convert_alpha()
        self.rect = 0
        self.size = size
        self.pos = pos
        
    def show(self, screen):
        img = pygame.transform.scale(self.image, self.size)
        self.rect = screen.blit(img, self.pos)
        
    def isClicked(self, pos):
        return self.rect.collidepoint(pos)
        
class DiceUi:
    def __init__(self, index, pos):
        self.index = index
        self.pos = pos
        self.diceValue = None
        self.diceState = DiceState.Inactive
        self.rect = ()
    
    def update(self, gameLogic):
        self.diceValue = gameLogic.getDiceValueAtPosition(self.index)
        self.diceState = gameLogic.getDiceStateAtPosition(self.index)
        
    def show(self, isAnimating, helper:UIHelper):        
        pos = self.pos
        if self.diceValue == None:
            self.diceValue = 1
            
        if self.diceState == DiceState.Unselected and isAnimating:
            self.diceValue = randint(1,6)
            pos = (pos[0] + randint(-2,2), pos[1] + randint(-2,2))
        
        dice = helper.getDiceImage(self.diceValue-1, True)
        
        match self.diceState:
            case DiceState.Inactive:
                dice.fill((30,205,205,0), special_flags=pygame.BLEND_RGBA_SUB)
            case DiceState.Selected:
                dice.fill((50,50,50,0), special_flags=pygame.BLEND_RGBA_SUB)
            
        self.rect = helper.blit(dice, pos)
        
        
    def isClicked(self, pos):
        return self.rect.collidepoint(pos)