import os
import pygame
PATH = os.path.abspath('.')+'/'
scale = 0.4
X = 8000*scale
Y = 8000*scale
scrn = pygame.display.set_mode((X, Y),pygame.FULLSCREEN | pygame.SCALED)
pygame.init()
board_img = pygame.transform.scale(pygame.image.load(PATH+'board.png').convert(),(8000*scale,8000*scale))
circle_img = pygame.transform.scale(pygame.image.load(PATH+'circle.png').convert_alpha(),(300*scale,300*scale))
selected_img = pygame.transform.scale(pygame.image.load(PATH+'selected.png').convert_alpha(),(990*scale,990*scale))
debag_img = pygame.transform.scale(pygame.image.load(PATH+'debag.png').convert_alpha(),(979.59*scale,979.59*scale))

pieces = {'bP': pygame.transform.scale(pygame.image.load(PATH+'bP.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'bfP': pygame.transform.scale(pygame.image.load(PATH+'bfP.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'wfP': pygame.transform.scale(pygame.image.load(PATH+'wfP.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'bk': pygame.transform.scale(pygame.image.load(PATH+'bN.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'bB': pygame.transform.scale(pygame.image.load(PATH+'bB.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'bR': pygame.transform.scale(pygame.image.load(PATH+'bR.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'bQ': pygame.transform.scale(pygame.image.load(PATH+'bQ.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'bK': pygame.transform.scale(pygame.image.load(PATH+'bK.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'wP': pygame.transform.scale(pygame.image.load(PATH+'wP.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'wk': pygame.transform.scale(pygame.image.load(PATH+'wN.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'wB': pygame.transform.scale(pygame.image.load(PATH+'wB.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'wR': pygame.transform.scale(pygame.image.load(PATH+'wR.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'wQ': pygame.transform.scale(pygame.image.load(PATH+'wQ.png').convert_alpha(),(979.59*scale,979.59*scale)),
          'wK': pygame.transform.scale(pygame.image.load(PATH+'wK.png').convert_alpha(),(979.59*scale,979.59*scale)),
          
          }


class rook():
    def __init__(self, cordinates, color, board):
        if valid_cordinates(cordinates):
            self.color = color
            self.cordinates = cordinates
            self.board = board
            if self.color == 'W':
                self.symbol = 'wR'
            elif self.color == 'B':
                self.symbol = 'bR'
        self.board.force_piece(cordinates, self)
        self.moved = False
    def check_move(self, cordinates):
        result = False
        if self.cordinates[0] == cordinates[0] and cordinates[1] != self.cordinates[1]:
            result = True
            for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                if not num == self.cordinates[1]:
                    piece = self.board.get_board_cell_info([self.cordinates[0], num])
                    if piece != None:
                        result = False
            if self.board.get_board_cell_info(cordinates) != None:
                if self.board.get_board_cell_info(cordinates).color == self.color:
                    result = False
        elif self.cordinates[1] == cordinates[1] and cordinates[0] != self.cordinates[0]:
            result = True
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            index_self = letters.index(self.cordinates[0])
            index = letters.index(cordinates[0])
            for letter_index in range(index_self, index, int((index-index_self)//abs(index-index_self))):
                letter = letters[letter_index]
                if not letter == self.cordinates[0]:
                    piece = self.board.get_board_cell_info([letter, self.cordinates[1]])
                    if piece != None:
                        result = False
            if self.board.get_board_cell_info(cordinates) != None:
                if self.board.get_board_cell_info(cordinates).color == self.color:
                    result = False
        return result
    def attacking_check(self, cordinates):
        result = False
        if self.cordinates[0] == cordinates[0] and cordinates[1] != self.cordinates[1]:
            result = True
            for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                if not num == self.cordinates[1]:
                    piece = self.board.get_board_cell_info([self.cordinates[0], num])
                    if piece != None:
                        result = False
        elif self.cordinates[1] == cordinates[1] and cordinates[0] != self.cordinates[0]:
            result = True
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            index_self = letters.index(self.cordinates[0])
            index = letters.index(cordinates[0])
            for letter_index in range(index_self, index, int((index-index_self)//abs(index-index_self))):
                letter = letters[letter_index]
                if not letter == self.cordinates[0]:
                    piece = self.board.get_board_cell_info([letter, self.cordinates[1]])
                    if piece != None:
                        result = False
        return result
    def move(self, cordinates):
        if self.check_move(cordinates):
            self.board.force_piece(self.cordinates, None)
            self.board.force_piece(cordinates, self)
            self.cordinates = cordinates
            self.moved = True

class bishop():
    def __init__(self, cordinates, color, board):
        if valid_cordinates(cordinates):
            self.color = color
            self.cordinates = cordinates
            self.board = board
            if self.color == 'W':
                self.symbol = 'wB'
            elif self.color == 'B':
                self.symbol = 'bB'
        self.board.force_piece(cordinates, self)
    def check_move(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        if cordinates == self.cordinates or self.cordinates[1] == cordinates[1] or self.cordinates[0] == cordinates[0]:
            return False
        result = False
        if abs((letters.index(self.cordinates[0]) - letters.index(cordinates[0]))/(self.cordinates[1] - cordinates[1])) == 1:
            result = True
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            index_self = letters.index(self.cordinates[0])
            index = letters.index(cordinates[0])
            letter_index = index_self
            for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                if index > letter_index or index < letter_index:
                    letter = letters[letter_index]
                    piece = self.board.get_board_cell_info([letter, num])
                    if piece != None and [letter, num] != self.cordinates:
                        result = False
                letter_index += int((index-index_self)//abs(index-index_self))
            if self.board.get_board_cell_info(cordinates) != None:
                if self.board.get_board_cell_info(cordinates).color == self.color:
                    result = False
        return result
    def attacking_check(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        if cordinates == self.cordinates or self.cordinates[1] == cordinates[1] or self.cordinates[0] == cordinates[0]:
            return False
        result = False
        if abs((letters.index(self.cordinates[0]) - letters.index(cordinates[0]))/(self.cordinates[1] - cordinates[1])) == 1:
            result = True
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            index_self = letters.index(self.cordinates[0])
            index = letters.index(cordinates[0])
            letter_index = index_self
            for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                if index > letter_index or index < letter_index:
                    letter = letters[letter_index]
                    piece = self.board.get_board_cell_info([letter, num])
                    if piece != None and [letter, num] != self.cordinates:
                        result = False
                letter_index += int((index-index_self)//abs(index-index_self))
        return result
    def move(self, cordinates):
        if self.check_move(cordinates):
            self.board.force_piece(self.cordinates, None)
            self.board.force_piece(cordinates, self)
            self.cordinates = cordinates

class knight():
    def __init__(self, cordinates, color, board):
        if valid_cordinates(cordinates):
            self.color = color
            self.cordinates = cordinates
            self.board = board
            if self.color == 'W':
                self.symbol = 'wk'
            elif self.color == 'B':
                self.symbol = 'bk'
        self.board.force_piece(cordinates, self)
    def check_move(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        distance = (letters.index(cordinates[0])-letters.index(self.cordinates[0]))**2+(cordinates[1]-self.cordinates[1])**2
        if distance == 5:
            if self.board.get_board_cell_info(cordinates) != None:
                if self.board.get_board_cell_info(cordinates).color != self.color:
                    return True
            else:
                return True
        return False
    def attacking_check(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        distance = (letters.index(cordinates[0])-letters.index(self.cordinates[0]))**2+(cordinates[1]-self.cordinates[1])**2
        if distance == 5:
            return True
        return False
    def move(self, cordinates):
        if self.check_move(cordinates):
            self.board.force_piece(self.cordinates, None)
            self.board.force_piece(cordinates, self)
            self.cordinates = cordinates

class queen():
    def __init__(self, cordinates, color, board):
        if valid_cordinates(cordinates):
            self.color = color
            self.cordinates = cordinates
            self.board = board
            if self.color == 'W':
                self.symbol = 'wQ'
            elif self.color == 'B':
                self.symbol = 'bQ'
        self.board.force_piece(cordinates, self)
    def check_move(self, cordinates):
        result = False
        if self.cordinates[0] == cordinates[0] and cordinates[1] != self.cordinates[1]:
            result = True
            for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                if not num == self.cordinates[1]:
                    piece = self.board.get_board_cell_info([self.cordinates[0], num])
                    if piece != None:
                        result = False
            if self.board.get_board_cell_info(cordinates) != None:
                if self.board.get_board_cell_info(cordinates).color == self.color:
                    result = False
        elif self.cordinates[1] == cordinates[1] and cordinates[0] != self.cordinates[0]:
            result = True
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            index_self = letters.index(self.cordinates[0])
            index = letters.index(cordinates[0])
            for letter_index in range(index_self, index, int((index-index_self)//abs(index-index_self))):
                letter = letters[letter_index]
                if not letter == self.cordinates[0]:
                    piece = self.board.get_board_cell_info([letter, self.cordinates[1]])
                    if piece != None:
                        result = False
            if self.board.get_board_cell_info(cordinates) != None:
                if self.board.get_board_cell_info(cordinates).color == self.color:
                    result = False
        
        
        if not result:
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            numbers = [1, 2, 3, 4, 5, 6, 7, 8]
            if cordinates == self.cordinates or self.cordinates[1] == cordinates[1] or self.cordinates[0] == cordinates[0]:
                return False
            result = False
            if abs((letters.index(self.cordinates[0]) - letters.index(cordinates[0]))/(self.cordinates[1] - cordinates[1])) == 1:
                result = True
                letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                index_self = letters.index(self.cordinates[0])
                index = letters.index(cordinates[0])
                letter_index = index_self
                for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                    if index > letter_index or index < letter_index:
                        letter = letters[letter_index]
                        piece = self.board.get_board_cell_info([letter, num])
                        if piece != None and [letter, num] != self.cordinates:
                            result = False
                    letter_index += int((index-index_self)//abs(index-index_self))
                if self.board.get_board_cell_info(cordinates) != None:
                    if self.board.get_board_cell_info(cordinates).color == self.color:
                        result = False
        return result
    def attacking_check(self, cordinates):
        result = False
        if self.cordinates[0] == cordinates[0] and cordinates[1] != self.cordinates[1]:
            result = True
            for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                if not num == self.cordinates[1]:
                    piece = self.board.get_board_cell_info([self.cordinates[0], num])
                    if piece != None:
                        result = False
        elif self.cordinates[1] == cordinates[1] and cordinates[0] != self.cordinates[0]:
            result = True
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            index_self = letters.index(self.cordinates[0])
            index = letters.index(cordinates[0])
            for letter_index in range(index_self, index, int((index-index_self)//abs(index-index_self))):
                letter = letters[letter_index]
                if not letter == self.cordinates[0]:
                    piece = self.board.get_board_cell_info([letter, self.cordinates[1]])
                    if piece != None:
                        result = False       
        if not result:
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            numbers = [1, 2, 3, 4, 5, 6, 7, 8]
            if cordinates == self.cordinates or self.cordinates[1] == cordinates[1] or self.cordinates[0] == cordinates[0]:
                return False
            result = False
            if abs((letters.index(self.cordinates[0]) - letters.index(cordinates[0]))/(self.cordinates[1] - cordinates[1])) == 1:
                result = True
                letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                index_self = letters.index(self.cordinates[0])
                index = letters.index(cordinates[0])
                letter_index = index_self
                for num in range(self.cordinates[1], cordinates[1], int((cordinates[1]-self.cordinates[1])//abs(cordinates[1]-self.cordinates[1]))):
                    if index > letter_index or index < letter_index:
                        letter = letters[letter_index]
                        piece = self.board.get_board_cell_info([letter, num])
                        if piece != None and [letter, num] != self.cordinates:
                            result = False
                    letter_index += int((index-index_self)//abs(index-index_self))
        return result
    def move(self, cordinates):
        if self.check_move(cordinates):
            self.board.force_piece(self.cordinates, None)
            self.board.force_piece(cordinates, self)
            self.cordinates = cordinates

class king():
    def __init__(self, cordinates, color, board):
        if valid_cordinates(cordinates):
            self.color = color
            self.cordinates = cordinates
            self.board = board
            if self.color == 'W':
                self.symbol = 'wK'
            elif self.color == 'B':
                self.symbol = 'bK'
        self.board.force_piece(cordinates, self)
        self.moved = False
    def check_move(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        distance = (letters.index(cordinates[0])-letters.index(self.cordinates[0]))**2+(cordinates[1]-self.cordinates[1])**2
        if self.board.get_board_cell_info(cordinates) != self:
            self.board.force_piece(self.cordinates, None)
            if self.board.get_board_cell_info(cordinates) != None:
                if self.board.get_board_cell_info(cordinates).color == self.color:
                    self.board.force_piece(self.cordinates, self)
                    return False
            if self.color == 'B':
                if not cordinates in self.board.get_attacking_map('W') and distance < 4:
                    self.board.force_piece(self.cordinates, self)
                    return True
            elif self.color == 'W':
                if not cordinates in self.board.get_attacking_map('B') and distance < 4:
                    self.board.force_piece(self.cordinates, self)
                    return True
        if self.color == 'W':
            if cordinates == ['C', 1]:
                if self.castling_A_side():
                    return True
            if cordinates == ['G', 1]:
                if self.castling_H_side():
                    return True
        if self.color == 'B':
            if cordinates == ['C', 8]:
                if self.castling_A_side():
                    return True
            if cordinates == ['G', 8]:
                if self.castling_H_side():
                    return True
        self.board.force_piece(self.cordinates, self)
        return False 
    def attacking_check(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        distance = (letters.index(cordinates[0])-letters.index(self.cordinates[0]))**2+(cordinates[1]-self.cordinates[1])**2
        if distance < 4:
            return True
        return False
    def move(self, cordinates):
        if self.color == 'W':
            if cordinates == ['C', 1]:
                if self.castling_A_side():
                    self.board.force_piece(['D', 1], self.board.get_board_cell_info(['A', 1]))
                    self.board.get_board_cell_info(['A', 1]).cordinates = ['D', 1]
                    self.board.force_piece(['A', 1], None)
                    self.board.force_piece(self.cordinates, None)
                    self.board.force_piece(cordinates, self)
                    self.cordinates = cordinates
                    self.moved = True
            if cordinates == ['G', 1]:
                if self.castling_H_side():
                    self.board.force_piece(['F', 1], self.board.get_board_cell_info(['H', 1]))
                    self.board.get_board_cell_info(['H', 1]).cordinates = ['F', 1]
                    self.board.force_piece(['H', 1], None)
                    self.board.force_piece(self.cordinates, None)
                    self.board.force_piece(cordinates, self)
                    self.cordinates = cordinates
                    self.moved = True
        if self.color == 'B':
            if cordinates == ['C', 8]:
                if self.castling_A_side():
                    self.board.force_piece(['D', 8], self.board.get_board_cell_info(['A', 8]))
                    self.board.get_board_cell_info(['A', 8]).cordinates = ['D', 8]
                    self.board.force_piece(['A', 8], None)
                    self.board.force_piece(self.cordinates, None)
                    self.board.force_piece(cordinates, self)
                    self.cordinates = cordinates
                    self.moved = True
            if cordinates == ['G', 8]:
                if self.castling_H_side():
                    self.board.force_piece(['F', 8], self.board.get_board_cell_info(['H', 8]))
                    self.board.get_board_cell_info(['H', 8]).cordinates = ['F', 8]
                    self.board.force_piece(['H', 8], None)
                    self.board.force_piece(self.cordinates, None)
                    self.board.force_piece(cordinates, self)
                    self.cordinates = cordinates
                    self.moved = True
        if self.check_move(cordinates):
            self.board.force_piece(self.cordinates, None)
            self.board.force_piece(cordinates, self)
            self.cordinates = cordinates
            self.moved = True
    def is_check(self):
        if self.color == 'B':
            if self.cordinates in self.board.get_attacking_map('W'):
                return True
        if self.color == 'W':
            if self.cordinates in self.board.get_attacking_map('B'):
                return True
        return False
    def castling_A_side(self):
        if not self.moved:
            if self.color == 'W':
                    attacking_map = self.board.get_attacking_map('B')
                    if ['E', 1] in attacking_map:
                        return False
                    for move in [['C', 1], ['D', 1]]:
                        if move in attacking_map or self.board.get_board_cell_info(move) != None:
                            return False
                    if self.board.get_board_cell_info(['A', 1]) != None:
                        if self.board.get_board_cell_info(['A', 1]).symbol == 'wR':
                            if not self.board.get_board_cell_info(['A', 1]).moved:
                                return True
            elif self.color == 'B':
                    attacking_map = self.board.get_attacking_map('W')
                    if ['E', 8] in attacking_map:
                        return False
                    for move in [['C', 8], ['D', 8]]:
                        if move in attacking_map or self.board.get_board_cell_info(move) != None:
                            return False
                    if self.board.get_board_cell_info(['A', 8]) != None:
                        if self.board.get_board_cell_info(['A', 8]).symbol == 'bR':
                            if not self.board.get_board_cell_info(['A', 8]).moved:
                                return True
        return False
    def castling_H_side(self):
        if not self.moved:
            if self.color == 'W':
                    attacking_map = self.board.get_attacking_map('B')
                    if ['E', 1] in attacking_map:
                        return False
                    for move in [['F', 1], ['G', 1]]:
                        if move in attacking_map or self.board.get_board_cell_info(move) != None:
                            return False
                    if self.board.get_board_cell_info(['H', 1]) != None:
                        if self.board.get_board_cell_info(['H', 1]).symbol == 'wR':
                            if not self.board.get_board_cell_info(['H', 1]).moved:
                                return True
            elif self.color == 'B':
                    attacking_map = self.board.get_attacking_map('W')
                    if ['E', 8] in attacking_map:
                        return False
                    for move in [['F', 8], ['G', 8]]:
                        if move in attacking_map or self.board.get_board_cell_info(move) != None:
                            return False
                    if self.board.get_board_cell_info(['H', 8]) != None:
                        if self.board.get_board_cell_info(['H', 8]).symbol == 'bR':
                            if not self.board.get_board_cell_info(['H', 8]).moved:
                                return True
        return False           

class pawn():
    def __init__(self, cordinates, color, board):
        if valid_cordinates(cordinates):
            self.color = color
            self.cordinates = cordinates
            self.board = board
            if self.color == 'W':
                self.symbol = 'wP'
            elif self.color == 'B':
                self.symbol = 'bP'
            self.board.force_piece(cordinates, self)
            self.en_passant = False
    def move(self, cordinates):
        if self.check_move(cordinates):
            if self.color == 'W':
                if cordinates[1] - self.cordinates[1] == 1:
                    if self.board.get_board_cell_info([cordinates[0], cordinates[1]-1]) != None:
                        if self.board.get_board_cell_info([cordinates[0], cordinates[1]-1]).symbol == 'bP':
                            if self.board.get_board_cell_info([cordinates[0], cordinates[1]-1]).en_passant:
                                self.board.force_piece([cordinates[0], cordinates[1]-1], None)
            elif self.color == 'B':
                if cordinates[1] - self.cordinates[1] == -1:
                    if self.board.get_board_cell_info([cordinates[0], cordinates[1]+1]) != None:
                        if self.board.get_board_cell_info([cordinates[0], cordinates[1]+1]).symbol == 'wP':
                            if self.board.get_board_cell_info([cordinates[0], cordinates[1]+1]).en_passant:
                                self.board.force_piece([cordinates[0], cordinates[1]+1], None)
            if abs(cordinates[1] - self.cordinates[1]) == 2:
                self.en_passant = True
            self.board.force_piece(self.cordinates, None)
            self.board.force_piece(cordinates, self)
            self.cordinates = cordinates
            if self.color == 'W' and self.cordinates[1] == 8:
                turning_pawn(self.cordinates, 'W', self.board)
            elif self.color == 'B' and self.cordinates[1] == 1:
                turning_pawn(self.cordinates, 'B', self.board)  
    def check_move(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if cordinates[0] == self.cordinates[0]: #Forward
            if self.color == "W":
                if cordinates[1] - self.cordinates[1] == 1:
                    if self.board.get_board_cell_info(cordinates) == None:
                        return True
                elif cordinates[1] - self.cordinates[1] == 2 and self.cordinates[1] == 2:
                    if self.board.get_board_cell_info(cordinates) == None and self.board.get_board_cell_info([cordinates[0], cordinates[1]-1]) == None:
                        return True
            if self.color == "B":
                if cordinates[1] - self.cordinates[1] == -1:
                    if self.board.get_board_cell_info(cordinates) == None:
                        return True
                elif cordinates[1] - self.cordinates[1] == -2 and self.cordinates[1] == 7:
                    if self.board.get_board_cell_info(cordinates) == None and self.board.get_board_cell_info([cordinates[0], cordinates[1]+1]) == None:
                        return True
        elif letters.index(cordinates[0]) + 1 == letters.index(self.cordinates[0]) or letters.index(cordinates[0])-1 == letters.index(self.cordinates[0]): #Takes
        
            if self.color == 'W':
                if cordinates[1] - self.cordinates[1] == 1:
                    if self.board.get_board_cell_info(cordinates) != None:
                        if self.board.get_board_cell_info(cordinates).color != self.color:
                            return True
                    if self.board.get_board_cell_info([cordinates[0], cordinates[1]-1]) != None:
                        if self.board.get_board_cell_info([cordinates[0], cordinates[1]-1]).symbol == 'bP':
                            if self.board.get_board_cell_info([cordinates[0], cordinates[1]-1]).en_passant:
                                return True
            elif self.color == 'B':
                if cordinates[1] - self.cordinates[1] == -1:
                    if self.board.get_board_cell_info(cordinates) != None:
                        if self.board.get_board_cell_info(cordinates).color != self.color:
                            return True
                    if self.board.get_board_cell_info([cordinates[0], cordinates[1]+1]) != None:
                        if self.board.get_board_cell_info([cordinates[0], cordinates[1]+1]).symbol == 'wP':
                            if self.board.get_board_cell_info([cordinates[0], cordinates[1]+1]).en_passant:
                                return True
        return False
    def attacking_check(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if letters.index(cordinates[0]) + 1 == letters.index(self.cordinates[0]) or letters.index(cordinates[0])-1 == letters.index(self.cordinates[0]): #Takes
            if self.color == 'W':
                if cordinates[1] - self.cordinates[1] == 1:
                    return True
            elif self.color == 'B':
                if cordinates[1] - self.cordinates[1] == -1:
                    return True
        return False
    def cancel_en_passant(self):
        self.en_passant = False

class turning_pawn():
    def __init__(self, cordinates, color, board):
        if valid_cordinates(cordinates):
            self.color = color
            self.cordinates = cordinates
            self.board = board
            if self.color == 'W':
                self.symbol = 'wfP'
            elif self.color == 'B':
                self.symbol = 'bfP'
            self.board.force_piece(cordinates, self)

class board():
    def __init__(self, playing_side, board=[]):
        self.board = list(board)
        self.playing_side = playing_side
        self.moves = []
        if self.board == []:
            self.highlited_piece = [None, None]
            for i in range(8):
                self.board.append([])
                for x in range(8):
                    self.board[i].append([None, None])
    def force_piece(self, cordinates, piece):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.board[letters.index(cordinates[0])][cordinates[1]-1][0] = piece
        if piece != None:
            self.board[letters.index(cordinates[0])][cordinates[1]-1][1] = piece.color
        else:
            self.board[letters.index(cordinates[0])][cordinates[1]-1][1] = None
    def print_board(self):
        
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' ']
        print(' 1 2 3 4 5 6 7 8', end='')
        x = 8
        for i in range(8):
            print('\n' + letters[i], end='')
            for x in range(8):
                self.board[i].append([None, None])
                if self.board[i][x][0] == None:
                    print('  ', end='')
                elif self.board[i][x][0] != None:
                    print(self.board[i][x][0].symbol, end='')
            print(letters[i], end='')
        print('\n 1 2 3 4 5 6 7 8')
    def gui_print(self):
        START_X = 81.63265304*scale
        START_Y = 81.63265304*scale
        END_X = 8000*scale-START_X
        END_Y = 8000*scale-START_Y
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        scrn.blit(board_img,(0,0))
    
        if self.playing_side == 'B':
            if self.highlited_piece != [None, None]:
                scrn.blit(selected_img, ((letters.index(self.highlited_piece[0])%8)*(END_X-START_X)/8+START_X, END_Y-(END_Y-START_Y)/8-(self.highlited_piece[1])*(END_Y-START_Y)/8))
            for move in self.get_attacking_map('W'):
                scrn.blit(debag_img, ((letters.index(move[0])%8)*(END_X-START_X)/8+START_X, END_Y-(END_Y-START_Y)//8-(move[1])*(END_Y-START_Y)//8))
            for letter in letters:
                for i in range(0,8):
                    piece = self.get_board_cell_info([letter, i+1])
                    if piece != None:
                        piece = self.get_board_cell_info([letter, i+1]).symbol
                        scrn.blit(pieces[str(piece)],((letters.index(letter)%8)*(END_X-START_X)/8+START_X, END_Y-(END_Y-START_Y)/8-(i)*(END_Y-START_Y)/8))
        if self.playing_side == 'W':
            if self.highlited_piece != [None, None]:
                scrn.blit(selected_img, ((letters.index(self.highlited_piece[0])%8)*(END_X-START_X)/8+START_X, END_Y-(END_Y-START_Y)/8-(self.highlited_piece[1]-1)*(END_Y-START_Y)/8))
            #for move in self.get_attacking_map('W'):
            #    scrn.blit(debag_img, ((letters.index(move[0])%8)*(END_X-START_X)//8+START_X, END_Y-(END_Y-START_Y)//8-(move[1]-1)*(END_Y-START_Y)//8))
            for letter in letters:
                for i in range(0,8):
                    piece = self.get_board_cell_info([letter, i+1])
                    if piece != None:
                        piece = self.get_board_cell_info([letter, i+1]).symbol
                        scrn.blit(pieces[str(piece)],((letters.index(letter)%8)*(END_X-START_X)/8+START_X, END_Y-(END_Y-START_Y)/8-(i)*(END_Y-START_Y)/8))
            #for i in range(7):
            #    i=i+1
            #    pygame.draw.line(scrn,WHITE,(0,i*97.959),(800,i*97.959))
            #    pygame.draw.line(scrn,WHITE,(i*97.959,0),(i*97.959,800))
        for move in self.moves:
            scrn.blit(circle_img,((letters.index(move[0])%8)*(END_X-START_X)//8+START_X+350*scale, END_Y-(END_Y-START_Y)//8-(move[1]-2)*(END_Y-START_Y)//8-650*scale))
        pygame.display.flip()
    def default_position(self):
        self.board = []
        for i in range(8):
            self.board.append([])
            for x in range(8):
                self.board[i].append([None, None])
        rook(['A',1], 'W',self)
        rook(['H',1],'W',self)
        rook(['A',8],'B',self)
        rook(['H',8],'B',self)

        knight(['B',1],'W',self)
        knight(['G',1],'W',self)
        knight(['B',8],'B',self)
        knight(['G',8],'B',self)
        
        bishop(['C',1],'W',self)
        bishop(['F',1],'W',self)
        bishop(['C',8],'B',self)
        bishop(['F',8],'B',self)

        king(['E',1],'W',self)
        queen(['D',1],'W',self)
        king(['E',8],'B',self)
        queen(['D',8],'B',self)
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(0,8):
            pawn([letters[i], 2],'W',self)
            pawn([letters[i], 7],'B',self)
    def highlite_piece(self, cordinates):
        if cordinates == [None, None]:
            return None
        piece = self.get_board_cell_info(cordinates)
        START_X = 8.163265304
        START_Y = 8.163265304
        END_X = 800-8.163265304
        END_Y = 800-8.163265304
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if piece != None:
            self.moves = possible_moves(piece)
            self.highlited_piece = cordinates
        else:
            self.moves = []
            self.highlited_piece = [None, None]
        self.gui_print()
    def get_board_cell_info(self, cordinates):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if cordinates[1]-1 < -1 or cordinates[1]-1 > 7:
        	return None
        return self.board[letters.index(cordinates[0])][cordinates[1]-1][0]
    def get_attacking_map(self, color):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        attacking_map = []
        for num in range(0,8):
            for letter in letters:
                if self.get_board_cell_info([letter, num]) != None:
                    if self.get_board_cell_info([letter, num]).color == color:
                        for move in attacking_moves(self.get_board_cell_info([letter, num])):
                            if move not in attacking_map:
                                attacking_map.append(move)
        return attacking_map
    def is_check_on_board(self, color):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for letter in letters:
            for i in range(0,8):
                piece = self.get_board_cell_info([letter, i+1])
                if piece != None:
                    if piece.symbol == color.lower()+"K":
                        return piece.is_check()
        raise "KING WASN'T FOUND!"
    def check_if_mate(self, color):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if self.is_check_on_board(color):
            for letter in letters:
                for i in range(0,8):
                    piece = self.get_board_cell_info([letter, i+1])
                    if piece != None:
                        if piece.color == color:
                            if len(possible_moves(piece)) != 0:
                                return False
            return True
        else:
            return False

def possible_moves(piece):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    moves = []
    for letter in letters:
        for i in range(1,9):
            if piece.check_move([letter, i]):
                moves.append([letter, i])
    if piece.symbol[1] == "K":
        moves_finall = moves
    else:
        moves_finall = try_moves_for_check(piece, moves, test_board.board)
    
    return moves_finall
def attacking_moves(piece):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    moves = []
    for letter in letters:
        for i in range(1,9):
            if piece.attacking_check([letter, i]):
                moves.append([letter, i])
    return moves
def cancel_en_passants(do_not_check):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    moves = []
    for letter in letters:
        for i in range(1,9):
            if test_board.get_board_cell_info([letter, i])!= None and not [letter, i] in do_not_check:
                if test_board.get_board_cell_info([letter, i]).symbol == 'bP' or test_board.get_board_cell_info([letter, i]).symbol == 'wP':
                    test_board.get_board_cell_info([letter, i]).cancel_en_passant()
    return moves
def valid_cordinates(cordinates):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    if cordinates[1] > 8 or cordinates[1] < 1 or not cordinates[0] in letters:
        raise "WRONG cordinates"
        return False
    else:
        return True
def try_moves_for_check(piece, moves, current_board):
    moves_preventing_check = []
    board_rn = current_board.copy()
    original_cordinates = piece.cordinates
    prevoius_cordinates = piece.cordinates
    prevoius_piece_taken = None
    for move in moves:
        temp_board = board('W', board_rn)
        prevoius_piece_taken = temp_board.get_board_cell_info(move)
        temp_board.force_piece(move, piece)
        temp_board.force_piece(original_cordinates, None)
        prevoius_cordinates = move
        if not temp_board.is_check_on_board(piece.color):
            moves_preventing_check.append(move)
        temp_board.force_piece(original_cordinates, piece)
        temp_board.force_piece(move, prevoius_piece_taken)
    return moves_preventing_check

test_board = board('W')
test_board.default_position()
'''
while True:
    test_board.gui_print('W')
    print(possible_moves(get_board_cell_info(['B',1])[0]))
    test_board.highlited_piece(['B',1])
    letter = input("Letter: ")
    num = int(input("Number: "))
    test_Knight.move([letter, num])'''
running = True

x = -1
en_passant_list = []
whose_move = 'W'
_50_move_rule_counter = 0
test_board.gui_print()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
    if x != -1:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        letter = (x-8)//(979*scale)
        if letter < 8 and letter >= 0:
            letter = letters[int((x-8)//(979*scale))]
        else:
            letter = None
        num = int(8-(y-8)//round(980*scale, 0))
        if letter == None:
            pass
        elif not [letter, num] in test_board.moves:
            if _50_move_rule_counter >= 50:
                pass
            elif test_board.highlited_piece == [letter, num]:
                test_board.moves = []
                test_board.highlited_piece = [None, None]
                test_board.gui_print()
            else:
                if test_board.get_board_cell_info([letter, num]) != None:
                    if test_board.get_board_cell_info([letter, num]).color == whose_move:
                        test_board.highlite_piece([letter, num])
                        test_board.gui_print()
                else:
                    test_board.highlite_piece([letter, num])
                    test_board.gui_print()            
        else:
            if test_board.get_board_cell_info(test_board.highlited_piece).symbol[1] == 'P' or test_board.get_board_cell_info([letter, num]) != None:
                    _50_move_rule_counter = 0
            test_board.get_board_cell_info(test_board.highlited_piece).move([letter, num])
            if test_board.get_board_cell_info([letter, num]) != None:
                if test_board.get_board_cell_info([letter, num]).symbol[1] == 'f':
                    done_choice = False
                    x = -1
                    test_board.moves = []
                    test_board.highlited_piece = [None, None]
                    test_board.gui_print()
                    while not done_choice:
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                done_choice = True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = pygame.mouse.get_pos()
                        if x != -1:
                            letter1 = round((x-8)//(979*scale), 0)
                            if letter1 < 8 and letter1 >= 0:
                                letter1 = letters[int((x-8)//(979*scale))]
                            num1 = 8-(y-8)//(979.59*scale)
                            #print(letter1, num1)
                            if [letter1, num1] == [letter, num]:
                                num2 = (y-8)//round(980*scale/2, 0)%2
                                letter2 = (x-8)//round(980*scale/2, 0)%2+1
                                #print(letter2, num2,'      ', letter1, num1)
                                if num2 == 0:
                                    if letter2 == 1:
                                        done_choice = True
                                        rook([letter, num], test_board.get_board_cell_info([letter, num]).color, test_board)
                                    if letter2 == 2:
                                        done_choice = True
                                        queen([letter, num], test_board.get_board_cell_info([letter, num]).color, test_board)
                                if num2 == 1:
                                    if letter2 == 1:
                                        done_choice = True
                                        knight([letter, num], test_board.get_board_cell_info([letter, num]).color, test_board)
                                    if letter2 == 2:
                                        done_choice = True
                                        bishop([letter, num], test_board.get_board_cell_info([letter, num]).color, test_board)
            _50_move_rule_counter += 0.5
            if _50_move_rule_counter >= 50:
                pass
            else:
                en_passant_list.append([letter, num])
                cancel_en_passants(en_passant_list)
                if len(en_passant_list) >= 1:
                    en_passant_list.pop(0)
                test_board.moves = []
                test_board.highlited_piece = [None, None]
                test_board.gui_print()
                if whose_move == 'W':
                    whose_move = 'B'
                else:
                    whose_move = 'W'
                if test_board.check_if_mate(whose_move):
                    pass
            
        x = -1
