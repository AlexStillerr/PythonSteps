#---------------------------------------------
# Dateiname: Kniffel.py
# Das Würfelspiel Kniffel in digitaler Form. Der Spieler kann bis zu 3 mal würfeln und sich dann
# aussuchen in welchem Feld er das Ergebnis eintragen möchte
# Autor: Alex Stiller
# Letzte Änderung: 10.09.2025
#---------------------------------------------
import pygame
from KniffelGameLogic import Kniffel
from KniffelGUI import KniffelGUI

class KniffelPygame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Kniffel")
        
        screenSize = (400, 800)
        self.gui = KniffelGUI(screenSize)
        
        self.clock = pygame.time.Clock()
        self.kniffel = Kniffel()
        self.isRunning = True
        self.isShaking = False

    def onShakerClicked(self):
        if self.isShaking:
            self.kniffel.roll()
            self.kniffel.checkRules()
            self.gui.updateValues(self.kniffel)
        else:
            self.kniffel.startShaking()
            self.gui.updateDices(self.kniffel)
        self.isShaking = not self.isShaking 

    def startGame(self):
        self.gui.updateValues(self.kniffel)
        self._runGameLoop()

    def _runGameLoop(self):
        while self.isRunning:
            self._handleEvents()           
        
            # Gamelogic
            # not needed
            
            # Ui
            self.gui.create(self.isShaking)
            self.gui.refresh()

            # refresh time
            self.clock.tick(60)
    
    def _handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            elif event.type == pygame.K_SPACE:
                print("Space pressed")
                self.onShakerClicked()
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handleMouseClick(pygame.mouse.get_pos())
            
    def _handleMouseClick(self, clickPos):
        if self.gui.shaker.isClicked(clickPos):
            self.onShakerClicked()
        elif self.gui.loadButton.isClicked(clickPos):
            print("Load")
        elif self.gui.saveButton.isClicked(clickPos):
            print("save")
        else:
            # TODO create events
            for i in range(5):
                if self.gui.diceObj[i].isClicked(clickPos):
                    self.kniffel.toggleDiceState(i)
                    self.gui.updateValues(self.kniffel)
                    break
            for e in self.gui.entries:
                if e.isClicked(clickPos) and self.kniffel.canScore(e.ruleId):
                    self.kniffel.addToScore(e.ruleId)
                    self.gui.playerScored(self.kniffel)
                    break
                
    def cleanup(self):
        pygame.quit()
        
        
if __name__ == "__main__":
    kniffel = KniffelPygame()
    kniffel.startGame()
    kniffel.cleanup()