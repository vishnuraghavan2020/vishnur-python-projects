import random


class WhitePiece(object):

    def __init__(self, cx, cy, typ = "white", possibleMoveLst = []):
        self.cx = cx
        self.cy = cy
        self.typ = typ
        self.possibleMoveLst = possibleMoveLst
        




    def attack(self, data, newRow, newCol):

        self.row = newRow
        self.col = newCol

        self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
        self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row


 

class WhitePawn(WhitePiece):
    
    def __init__(self, cx, cy, col, row = 1, radius = 10, color = "white", firstMove = True):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        filename = "chess_pieces/white_pawn.gif"
        self.image = PhotoImage(file = filename)
        self.firstMove = firstMove


    def __repr__(self):
        return "%s" % ("White Pawn")


    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow,newCol))
         



    def allowMove(self, data, newRow, newCol):

        if data.inWhiteCheck == False:

            
            if self.firstMove == True:

                if newRow - self.row <= 2 and self.col == newCol:
                    if data.board[newRow][newCol] == False:
                        return True

            elif self.firstMove == False:

                if newRow - self.row == 1 and self.col == newCol:

                    if data.board[newRow][newCol] == False:
                        return True

                return False

        
       
    def move(self, data, newRow, newCol):


        if data.currPress != None:
            if self.firstMove == True:

                if (newRow - self.row >= 0 and newRow - self.row <= 2) and (self.col == newCol):

                    self.row = newRow
                
                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row

            elif self.firstMove == False:


                if (newRow - self.row >= 0 and newRow - self.row <= 1) and (self.col == newCol):
 
                    self.row = newRow
                    

                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row




    def canAttack(self, data, newRow, newCol, other):

        if data.inWhiteCheck == False:

            if self.typ != other.typ and repr(other) != "Black King":
                if other.row == newRow and other.col == newCol:
                    if other.row - self.row == 1 and abs(other.col - self.col) == 1:

                        return True

                    return False


    
    def doCheck(self, data, other):
        

        if repr(other) == "Black King" and other.row - self.row == 1 and abs(other.col - self.col) == 1:
            return True

        else:

            return False

        

    def draw(self, canvas):

    
        canvas.create_image(self.cx, self.cy, image = self.image)


                
class WhiteKing(WhitePiece):

    def __init__(self, cx, cy, col = 4, row = 0, radius = 10, color = "white", direc = [1,1], canCastle = True):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/white_king.gif"
        self.image = PhotoImage(file = filename)
        self.canCastle = canCastle



    def __repr__(self):

        return "%s" % ("White King")


    def inCheck(self, data, other):


        if repr(other) != "White King" and repr(other) != "Black King":
            if other.doCheck(data, self) == True:

                data.inWhiteCheck = True

                
                return True

        data.inWhiteCheck = False
    
        return False


    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                


    


    def allowMove(self, data, newRow, newCol):

    
        if newRow != self.row and newCol != self.col:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newRow == self.row and newCol != self.col:

            self.direc[0] = 0
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newCol == self.col and newRow != self.row:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = 0




        if self.canCastle == True:

            for other in data.initialPieces:

                if repr(other) == "White Rook":

                    if other.row == newRow and other.col == newCol:

                        tempRow1 = self.row 
                        tempCol1 = self.col 

                        tempRow2 = other.row 
                        tempCol2 = other.col

              

                        if data.board[newRow][newCol] == True:
                            
                            return True





            if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:


                if self.direc == [1, 1] or self.direc == [-1,-1] or \
                self.direc == [1,-1] or self.direc == [-1,1] or self.direc == [1,0] or \
                self.direc == [0,1] or self.direc == [-1,0] or self.direc == [0,-1]:



                    if data.board[newRow][newCol] == True:
                        return False

                    else:
                        return True


        elif self.canCastle == False:


            if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:

                    if self.direc == [1, 1] or self.direc == [-1,-1] or \
                    self.direc == [1,-1] or self.direc == [-1,1] or self.direc == [1,0] or \
                    self.direc == [0,1] or self.direc == [-1,0] or self.direc == [0,-1]:



                        if data.board[newRow][newCol] == True:
                            return False

                        else:
                            return True





    def move(self, data, newRow, newCol):

        if data.currPress != None:

            if self.canCastle == True:

                for other in data.initialPieces:
                    if repr(other) == "White Rook":
                        if other.row == newRow and other.col == newCol:

                            tempRow1 = self.row 
                            tempCol1 = self.col 

                            tempRow2 = other.row 
                            tempCol2 = other.col 

                            self.row = tempRow2 
                            self.col = tempCol2 
                            other.row = tempRow1 
                            other.col = tempCol1



                            self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                            self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row

                            other.cx = data.margin + data.cellWidth//2 + data.cellWidth*other.col
                            other.cy = data.margin + data.cellWidth//2 + data.cellWidth*other.row
                                



                if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:

        
                    self.row = newRow
                    self.col = newCol
                    

                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row

            if self.canCastle == False:



                if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:

            
                    self.row = newRow
                    self.col = newCol
                    

                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row





    def canAttack(self, data, newRow, newCol, other):

        if data.inWhiteCheck == False:


            if self.typ != other.typ and repr(other) != "Black King":

                if other.row == newRow and other.col == newCol:

                    if other.doCheck(data, self) == False:

            
                        if (abs(other.row - self.row) == 1 and abs(other.col - self.col) == 1) or (abs(other.row - self.row) == 0 and abs(other.col - self.col) == 1) or \
                        (abs(other.row - self.row) == 1 and abs(other.col - self.col) == 0):

                            return True

                        return False
            


    def draw(self, canvas):

        canvas.create_image(self.cx, self.cy, image = self.image)



class WhiteQueen(WhitePiece):
    def __init__(self, cx, cy, col = 3, row = 0, radius = 10, color = "white", direc = [1,1]):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/white_queen.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("White Queen")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                

    def doCheck(self, data, other):

        if other.row != self.row and other.col != self.col:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)

        elif other.row == self.row and other.col != self.col:

            self.direc[0] = 0
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)

        elif other.col == self.col and other.row != self.row:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = 0

        if repr(other) == "Black King":

            
            if self.direc == [1,0] or self.direc == [-1,0]:
                if self.col == other.col:

                    for row in range(self.row + self.direc[0], other.row, self.direc[0]):
                        if data.board[row][other.col] == True:
                            return False

                    return True

            if self.direc == [0,1] or self.direc == [0,-1]:
                if self.row == other.row:

                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):
                        if data.board[self.row][col] == True:
                            return False
                    return True



        
            if self.direc == [1,-1] or self.direc == [-1,1]:


                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row + col == self.row + self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row + col == self.row + self.col:

                            if other.row == row and other.col == col:
                                return True

                return False


            
            if self.direc == [1,1] or self.direc == [-1,-1]:

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row - col == self.row - self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row - col == self.row - self.col:

                            if other.row == row and other.col == col:
                                return True

                return False




    def allowMove(self, data, newRow, newCol):

        if data.inWhiteCheck == False:

            if newRow != self.row and newCol != self.col:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

            elif newRow == self.row and newCol != self.col:

                self.direc[0] = 0
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

            elif newCol == self.col and newRow != self.row:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = 0



            if self.direc == [1,-1] or self.direc == [-1, 1]:

                if self.row + self.col == newRow + newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                            if row + col == self.row + self.col:

                                if data.board[row][col] == True:
                                    return False

                    return True

                        

            if self.direc == [1,1] or self.direc == [-1, -1]:

                if self.row - self.col == newRow - newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                            if row - col == self.row - self.col:

                                if data.board[row][col] == True:
                                    return False

                    return True


            if self.direc == [0,1] or self.direc == [0,-1]:

                if self.row == newRow:

                    for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                        if data.board[self.row][col] == True:
                                return False

                    return True


            if self.direc == [1,0] or self.direc == [-1,0]:

                if self.col == newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):

                        if data.board[row][self.col] == True:
                            return False

                    
                    return True



    def move(self, data, newRow, newCol):

        if data.currPress != None:

            if (abs(newRow - self.row) == abs(newCol - self.col)) or (abs(newRow - self.row) <= 8 and self.col == newCol) or (abs(newCol - self.col) <= 8 and self.row == newRow) or (abs(newRow - self.row) == abs(newCol - self.col)):


        
                self.row = newRow
                self.col = newCol
                

                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row



    def attackHelper(self, data, newRow, newCol):

        if newRow != self.row and newCol != self.col:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newRow == self.row and newCol != self.col:

            self.direc[0] = 0
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newCol == self.col and newRow != self.row:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = 0



        if self.direc == [1,-1] or self.direc == [-1, 1]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                    if row + col == self.row + self.col:

                        if data.board[row][col] == True:
                            return False

            return True

                    

        if self.direc == [1,1] or self.direc == [-1, -1]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                    if row - col == self.row - self.col:

                        if data.board[row][col] == True:
                            return False

            return True


        if self.direc == [0,1] or self.direc == [0,-1]:
            for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                if data.board[self.row][col] == True:
                        return False

            return True


        if self.direc == [1,0] or self.direc == [-1,0]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):

                if data.board[row][self.col] == True:
                    return False

                
            return True

        



    def canAttack(self, data, newRow, newCol, other):

        if data.inWhiteCheck == False:

            if self.typ != other.typ and repr(other) != "Black King":

                if other.row == newRow and other.col == newCol:

                    if self.attackHelper(data, newRow, newCol) == True:

                        return True

                    return False


    def draw(self, canvas):
    
        canvas.create_image(self.cx, self.cy, image = self.image)



class WhiteBishop(WhitePiece):
    def __init__(self, cx, cy, col, row = 0, radius = 10, color = "white", direc = [1,1]):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/white_bishop.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("White Bishop")


    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                


    def doCheck(self, data, other):

        if other.row != self.row and other.col != self.col:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)

    

        if repr(other) == "Black King":

            
      
            if self.direc == [1,-1] or self.direc == [-1,1]:


                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row + col == self.row + self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row + col == self.row + self.col:

                            if other.row == row and other.col == col:
                                return True

                return False


            
            if self.direc == [1,1] or self.direc == [-1,-1]:

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row - col == self.row - self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row - col == self.row - self.col:

                            if other.row == row and other.col == col:
                                return True

                return False

        

        


    def allowMove(self, data, newRow, newCol):

        if data.inWhiteCheck == False:


            if newRow != self.row and newCol != self.col:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)



            if self.direc == [1,-1] or self.direc == [-1, 1]:

                if self.row + self.col == newRow + newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                            if row + col == self.row + self.col:

            
                                if data.board[row][col] == True:
                                    return False

                    return True


            elif self.direc == [1,1] or self.direc == [-1, -1]:

                if self.row - self.col == newRow - newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                            if row - col == self.row - self.col:
                           
                                if data.board[row][col] == True:
                          
                                   return False
                        

                    return True

            else:
                return False

    
    def move(self, data, newRow, newCol):

        if data.currPress != None:
            
            if abs(newRow - self.row) == abs(newCol - self.col):
                  
                self.row = newRow
                self.col = newCol
     
                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row



    def attackHelper(self, data, newRow, newCol):

        if newRow != self.row and newCol != self.col:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)




        if self.direc == [1,-1] or self.direc == [-1, 1]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                    if row + col == self.row + self.col:
                        
                        if data.board[row][col] == True:

                            return False

            return True

                    

 

        if self.direc == [1,1] or self.direc == [-1, -1]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                    if row - col == self.row - self.col:
                   
                        if data.board[row][col] == True:
                            return False

        
            return True



    
    def canAttack(self, data, newRow, newCol, other):

        if data.inWhiteCheck == False:

            if self.typ != other.typ and repr(other) != "Black King":

                if other.row == newRow and other.col == newCol:

                    if self.attackHelper(data, newRow, newCol) == True:
       
                        return True

                    return False


    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image = self.image)



class WhiteKnight(WhitePiece):
    def __init__(self, cx, cy, col, row = 0, radius = 10, color = "white"):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col

        filename = "chess_pieces/white_knight.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("White Knight")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                


    def doCheck(self, data, other):

        if repr(other) == "Black King":
        
            if (abs(other.row - self.row) == 1 and abs(other.col - self.col) == 2) or (abs(other.row - self.row) == 2 and abs(other.col - self.col) == 1):
                return True

            return False

        


    def allowMove(self, data, newRow, newCol):

        if data.inWhiteCheck == False:

            if (abs(newRow - self.row) == 1 and abs(newCol - self.col) == 2) or (abs(newRow - self.row) == 2 and abs(newCol - self.col) == 1):

                if data.board[newRow][newCol] == True:
                    return False

                else:

                    return True




    def move(self, data, newRow, newCol):

        if data.currPress != None:


            if (abs(newRow - self.row) == 1 and abs(newCol - self.col) == 2) or (abs(newRow - self.row) == 2 and abs(newCol - self.col) == 1):

        
                self.row = newRow
                self.col = newCol
                

                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row




    def attackHelper(self, data, newRow, newCol):

        if (abs(newRow - self.row) == 1 and abs(newCol - self.col) == 2) or (abs(newRow - self.row) == 2 and abs(newCol - self.col) == 1):
        
            if data.board[newRow][newCol] == True:
                return True

        return False


    def canAttack(self, data, newRow, newCol, other):

        if data.inWhiteCheck == False:

        
            if self.typ != other.typ and repr(other) != "Black King":

                if other.row == newRow and other.col == newCol:

                    if self.attackHelper(data, newRow, newCol) == True:

                        return True

                    return False


    def draw(self, canvas):

        canvas.create_image(self.cx, self.cy, image = self.image)



class WhiteRook(WhitePiece):
    def __init__(self, cx, cy, col, row = 0, radius = 10, color = "white", direc = [1,0]):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/white_rook.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("White Rook")

    def getPossibleMoves(self, data, newRow, newCol):


        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:
                
                self.possibleMoveLst.append((newRow, newCol))
                

        
       

    def doCheck(self, data, other):


        if other.row == self.row and other.col != self.col:

            self.direc[0] = 0
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)

        elif other.col == self.col and other.row != self.row:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = 0

        if repr(other) == "Black King":


            if self.direc == [1,0] or self.direc == [-1,0]:
                if self.col == other.col:

                    for row in range(self.row + self.direc[0], other.row, self.direc[0]):
                        if data.board[row][other.col] == True:
                            return False

                    return True

            if self.direc == [0,1] or self.direc == [0,-1]:
                if self.row == other.row:

                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):
                        if data.board[self.row][col] == True:
                            return False
                    return True


    


    def allowMove(self, data, newRow, newCol):

        if data.inWhiteCheck == False:

            
            if newRow == self.row and newCol != self.col:

                self.direc[0] = 0
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

            elif newCol == self.col and newRow != self.row:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = 0




            if self.direc == [0,1] or self.direc == [0,-1]:
                if self.row == newRow:
                
                    for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                        if data.board[newRow][col] == True:
                            return False
                
                    return True
                


            elif self.direc == [1,0] or self.direc == [-1,0]:
                if self.col == newCol:
                
                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        
                        if data.board[row][newCol] == True or newCol != self.col:
                            return False

                    return True

            else:
                return False

                

            




    def move(self, data, newRow, newCol):

        if data.currPress != None:

            if (abs(newRow - self.row) <= 8 and self.col == newCol) or (abs(newCol - self.col) <= 8 and self.row == newRow):

                self.row = newRow
                self.col = newCol
                
                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row



    def attackHelper(self, data, newRow, newCol):


        if newRow == self.row and newCol != self.col:

            self.direc[0] = 0
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newCol == self.col and newRow != self.row:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = 0


        if self.direc == [0,1] or self.direc == [0,-1]:
            for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                if data.board[self.row][col] == True:
                        return False

            return True


        if self.direc == [1,0] or self.direc == [-1,0]:
            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                
                if data.board[row][self.col] == True:
                    return False


            return True


    def canAttack(self, data, newRow, newCol, other):

        if data.inWhiteCheck == False:
        
            if self.typ != other.typ and repr(other) != "Black King":

                if other.row == newRow and other.col == newCol:

                    if self.attackHelper(data, newRow, newCol) == True:

                        return True
                    return False


    def draw(self, canvas):

        canvas.create_image(self.cx, self.cy, image = self.image)


#______________________________________________________________________________________

class BlackPiece(object):

    def __init__(self, cx, cy, typ = "black", possibleMoveLst = []):
        self.cx = cx
        self.cy = cy
        self.typ = typ
        self.possibleMoveLst = possibleMoveLst
        



    def attack(self, data, newRow, newCol):

        self.row = newRow
        self.col = newCol

        self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
        self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row



class BlackPawn(BlackPiece):
    
    def __init__(self, cx, cy, col, row = 6, radius = 10, color = "gray", firstMove = True):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        filename = "chess_pieces/black_pawn.gif"
        self.image = PhotoImage(file = filename)
        self.firstMove = firstMove


    def __repr__(self):
        return "%s" % ("Black Pawn")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
               



    def allowMove(self, data, newRow, newCol):

        if data.inBlackCheck == False:
            if self.firstMove == True:
                if self.row - newRow <= 2 and self.col == newCol:
                    if data.board[newRow][newCol] == False:
                        return True


        elif self.firstMove == False:

            if self.row - newRow == 1 and self.col == newCol:
                if data.board[newRow][newCol] == False:
                    return True

            return False

        

    def move(self, data, newRow, newCol):

        if data.currPress != None:
            if self.firstMove == True:
                if (self.row - newRow >= 0 and self.row - newRow <= 2) and (self.col == newCol):

                    self.row = newRow
                  
                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row


            elif self.firstMove == False:

                if (self.row - newRow >= 0 and self.row - newRow <= 1) and (self.col == newCol):     
                    self.row = newRow
                    
                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row



    def canAttack(self, data, newRow, newCol, other):

        if data.inBlackCheck == False:
            if self.typ != other.typ and repr(other) != "White King":
                if other.row == newRow and other.col == newCol:
                    if self.row - other.row == 1 and abs(other.col - self.col) == 1:

                        return True

                    return False



    def doCheck(self, data, other):

        if repr(other) == "White King" and self.row - other.row == 1 and abs(other.col - self.col) == 1:
            return True

        else:

            return False

        

    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image = self.image)


               
class BlackKing(BlackPiece):

    def __init__(self, cx, cy, col = 3, row = 7, radius = 10, color = "gray", direc = [-1,1], canCastle = True):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/black_king.gif"
        self.image = PhotoImage(file = filename)
        self.canCastle = canCastle


    def __repr__(self):

        return "%s" % ("Black King")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                


    def inCheck(self, data, other):
        
        if repr(other) != "White King" and repr(other) != "Black King":
            if other.doCheck(data, self) == True:
                data.inBlackCheck == True
                return True

        data.inBlackCheck = False

        return False


    

    def allowMove(self, data, newRow, newCol):


        if newRow != self.row and newCol != self.col:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newRow == self.row and newCol != self.col:

            self.direc[0] = 0
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newCol == self.col and newRow != self.row:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = 0


        if self.canCastle == True:

            for other in data.initialPieces:

                if repr(other) == "Black Rook":

                    if other.row == newRow and other.col == newCol:

                        tempRow1 = self.row 
                        tempCol1 = self.col 

                        tempRow2 = other.row 
                        tempCol2 = other.col

                        
                        if data.board[newRow][newCol] == True:
                            
                            return True


            if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:


                if self.direc == [1, 1] or self.direc == [-1,-1] or \
                self.direc == [1,-1] or self.direc == [-1,1] or self.direc == [1,0] or \
                self.direc == [0,1] or self.direc == [-1,0] or self.direc == [0,-1]:


                    if data.board[newRow][newCol] == True:
                        return False

                    else:
                        return True


        elif self.canCastle == False:

            if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:

                    if self.direc == [1, 1] or self.direc == [-1,-1] or \
                    self.direc == [1,-1] or self.direc == [-1,1] or self.direc == [1,0] or \
                    self.direc == [0,1] or self.direc == [-1,0] or self.direc == [0,-1]:


                        if data.board[newRow][newCol] == True:
                            return False

                        else:
                            return True

        

    def move(self, data, newRow, newCol):

        if data.currPress != None:
            if self.canCastle == True:

                for other in data.initialPieces:
                    if repr(other) == "Black Rook":
                        if other.row == newRow and other.col == newCol:

                            tempRow1 = self.row 
                            tempCol1 = self.col 

                            tempRow2 = other.row 
                            tempCol2 = other.col 

                            self.row = tempRow2 
                            self.col = tempCol2 
                            other.row = tempRow1 
                            other.col = tempCol1


                            self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                            self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row

                            other.cx = data.margin + data.cellWidth//2 + data.cellWidth*other.col
                            other.cy = data.margin + data.cellWidth//2 + data.cellWidth*other.row
                                

                if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:

        
                    self.row = newRow
                    self.col = newCol
                    
                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row

            if self.canCastle == False:

                if abs(newRow - self.row) <= 1 and abs(newCol - self.col) <= 1:
            
                    self.row = newRow
                    self.col = newCol
                    
                    self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                    self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row


    def canAttack(self, data, newRow, newCol, other):

    
        if self.typ != other.typ and repr(other) != "White King":
            if other.doCheck(data, other) == False:
                if other.row == newRow and other.col == newCol:

                    if (abs(other.row - self.row) == 1 and abs(other.col - self.col) == 1) or (abs(other.row - self.row) == 0 and abs(other.col - self.col) == 1) or \
                    (abs(other.row - self.row) == 1 and abs(other.col - self.col) == 0):

                        return True
                    return False

    def draw(self, canvas):

        canvas.create_image(self.cx, self.cy, image = self.image)



            
class BlackQueen(BlackPiece):
    def __init__(self, cx, cy, col = 4, row = 7, radius = 10, color = "light grey", direc = [-1,1]):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/black_queen.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("Black Queen")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                


    def doCheck(self, data, other):


        if other.row != self.row and other.col != self.col:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)

        elif other.row == self.row and other.col != self.col:

            self.direc[0] = 0
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)

        elif other.col == self.col and other.row != self.row:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = 0

        if repr(other) == "White King":

    
            if self.direc == [1,0] or self.direc == [-1,0]:
                if self.col == other.col:

                    for row in range(self.row + self.direc[0], other.row, self.direc[0]):
                        if data.board[row][other.col] == True:
                            return False

                    return True

            if self.direc == [0,1] or self.direc == [0,-1]:
                if self.row == other.row:

                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):
                        if data.board[self.row][col] == True:
                            return False
                    return True

        
            if self.direc == [1,-1] or self.direc == [-1,1]:


                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row + col == self.row + self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row + col == self.row + self.col:

                            if other.row == row and other.col == col:
                                return True

                return False


            
            if self.direc == [1,1] or self.direc == [-1,-1]:

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row - col == self.row - self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row - col == self.row - self.col:

                            if other.row == row and other.col == col:
                                return True

                return False



    def allowMove(self, data, newRow, newCol):

        if data.inBlackCheck == False:

            if newRow != self.row and newCol != self.col:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

            elif newRow == self.row and newCol != self.col:

                self.direc[0] = 0
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

            elif newCol == self.col and newRow != self.row:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = 0

           

            if self.direc == [1,-1] or self.direc == [-1, 1]:

                if self.row + self.col == newRow + newCol:


                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                       for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                            if row + col == self.row + self.col:
                                if data.board[row][col] == True:
                                    return False

                    return True


            if self.direc == [1,1] or self.direc == [-1, -1]:

                if self.row - self.col == newRow - newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                       for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                            if row - col == self.row - self.col:
                                if data.board[row][col] == True:
                                    return False

                    return True


            
            if self.direc == [0,1] or self.direc == [0,-1]:

                if self.row == newRow:
                
                    for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):
                        if data.board[self.row][col] == True:
                            return False

                    return True



            if self.direc == [1,0] or self.direc == [-1,0]:

                if self.col == newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        if data.board[row][self.col] == True:
                            return False

                        
                    return True



    def move(self, data, newRow, newCol):

        if data.currPress != None:

            if (abs(newRow - self.row) == abs(newCol - self.col)) or (abs(newRow - self.row) <= 8 and self.col == newCol) or (abs(newCol - self.col) <= 8 and self.row == newRow) or (abs(newRow - self.row) == abs(newCol - self.col)):
        
                self.row = newRow
                self.col = newCol
                

                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row


    def attackHelper(self, data, newRow, newCol):

        if newRow != self.row and newCol != self.col:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newRow == self.row and newCol != self.col:

            self.direc[0] = 0
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newCol == self.col and newRow != self.row:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = 0


        if self.direc == [1,-1] or self.direc == [-1, 1]:


            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
               for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                    if row + col == self.row + self.col:
                        if data.board[row][col] == True:
                            return False

            return True


        if self.direc == [1,1] or self.direc == [-1, -1]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
               for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                    if row - col == self.row - self.col:
                        if data.board[row][col] == True:
                            return False

            return True


        
        if self.direc == [0,1] or self.direc == [0,-1]:
            
            for col in range(self.col + self.direc[1], newCol, self.direc[1]):
                if data.board[self.row][col] == True:
                    return False

            return True


        if self.direc == [1,0] or self.direc == [-1,0]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                if data.board[row][self.col] == True:
                    return False

                
            return True


    def canAttack(self, data, newRow, newCol, other):

        if data.inBlackCheck == False:

            if self.typ != other.typ and repr(other) != "White King":

                if other.row == newRow and other.col == newCol:

                    if self.attackHelper(data, newRow, newCol) == True:

                        return True
                    return False


    def draw(self, canvas):

        canvas.create_image(self.cx, self.cy, image = self.image)



class BlackBishop(BlackPiece):
    def __init__(self, cx, cy, col, row = 7, radius = 10, color = "light grey", direc = [1,1]):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/black_bishop.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("Black Bishop")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                


    def doCheck(self, data, other):

        if other.row != self.row and other.col != self.col:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)
   

        if repr(other) == "White King":
        
            if self.direc == [1,-1] or self.direc == [-1,1]:

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row + col == self.row + self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row + col == self.row + self.col:

                            if other.row == row and other.col == col:
                                return True

                return False


            
            if self.direc == [1,1] or self.direc == [-1,-1]:

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):

                        if row - col == self.row - self.col:
                          
                            if data.board[row][col] == True:
                                return False

                for row in range(self.row + self.direc[0], other.row + self.direc[0], self.direc[0]):
                    for col in range(self.col + self.direc[1], other.col + self.direc[1], self.direc[1]):

                        if row - col == self.row - self.col:

                            if other.row == row and other.col == col:
                                return True

                return False



    def allowMove(self, data, newRow, newCol):

        if data.inBlackCheck == False:

            if newRow != self.row and newCol != self.col:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)


            if self.direc == [1,-1] or self.direc == [-1, 1]:

                if self.row + self.col == newRow + newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

            
                            if row + col == self.row + self.col:

                                if data.board[row][col] == True:
                                    return False

                    return True



            if self.direc == [1,1] or self.direc == [-1, -1]:

                if self.row - self.col == newRow - newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):
                        for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):

                            if row - col == self.row - self.col:

                                if data.board[row][col] == True:
                                    return False

         
                    return True

    

    def move(self, data, newRow, newCol):

        if data.currPress != None:

            
            if abs(newRow - self.row) == abs(newCol - self.col):
        
                self.row = newRow
                self.col = newCol

            
                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row



    def attackHelper(self, newRow, newCol):

        if newRow != self.row and newCol != self.col:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

    
        if self.direc == [1,-1] or self.direc == [-1, 1]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                for col in range(self.col + self.direc[1], newCol, self.direc[1]):

    
                    if row + col == self.row + self.col:

                        if data.board[row][col] == True:
                            return False

            return True



        if self.direc == [1,1] or self.direc == [-1, -1]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):
                for col in range(self.col + self.direc[1], newCol, self.direc[1]):

                    if row - col == self.row - self.col:

                        if data.board[row][col] == True:
                            return False

 
            return True


    def canAttack(self, data, newRow, newCol, other):

        if data.inBlackCheck == False:

            if self.typ != other.typ and repr(other) != "White King":

                if other.row == newRow and other.col == newCol:

                    if self.attackHelper(data, newRow, newCol) == True:

                        return True

                    return False



    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image = self.image)



class BlackKnight(BlackPiece):
    def __init__(self, cx, cy, col, row = 7, radius = 10, color = "light grey"):
        super().__init__(cx, cy, possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        filename = "chess_pieces/black_knight.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("Black Knight")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:


                self.possibleMoveLst.append((newRow, newCol))
                


    def doCheck(self, data, other):

        if repr(other) == "White King":
            if (abs(other.row - self.row) == 1 and abs(other.col - self.col) == 2) or (abs(other.row - self.row) == 2 and abs(other.col - self.col) == 1):
                return True

            return False
        



    def allowMove(self, data, newRow, newCol):

        if data.inBlackCheck == False:

            if (abs(newRow - self.row) == 1 and abs(newCol - self.col) == 2) or (abs(newRow - self.row) == 2 and abs(newCol - self.col) == 1):
                if data.board[newRow][newCol] == True:
                    return False

                else:

                    return True


    def move(self, data, newRow, newCol):

        if data.currPress != None:


            if (abs(newRow - self.row) == 1 and abs(newCol - self.col) == 2) or (abs(newRow - self.row) == 2 and abs(newCol - self.col) == 1):

        
                self.row = newRow
                self.col = newCol
                
                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row




    def attackHelper(self, data, newRow, newCol):

        if (abs(newRow - self.row) == 1 and abs(newCol - self.col) == 2) or (abs(newRow - self.row) == 2 and abs(newCol - self.col) == 1):
        
            if data.board[newRow][newCol] == True:
                return True

        return False


    def canAttack(self, data, newRow, newCol, other):

        if data.inBlackCheck == False:
        
            if self.typ != other.typ and repr(other) != "White King":

                if other.row == newRow and other.col == newCol:
                    if self.attackHelper(data, newRow, newCol) == True:
                        return True
                    return False



    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image = self.image)


class BlackRook(BlackPiece):
    def __init__(self, cx, cy, col, row = 7, radius = 10, color = "light grey", direc = [1,0]):
        super().__init__(cx, cy,possibleMoveLst = [])

        self.radius = radius
        self.row = row
        self.col = col
        self.direc = direc
        filename = "chess_pieces/black_rook.gif"
        self.image = PhotoImage(file = filename)


    def __repr__(self):

        return "%s" % ("Black Rook")

    def getPossibleMoves(self, data, newRow, newCol):

        if data.board[newRow][newCol] == False:
            if self.allowMove(data, newRow, newCol) == True:

                self.possibleMoveLst.append((newRow, newCol))
                


    def doCheck(self, data, other):

    
        if other.row == self.row and other.col != self.col:

            self.direc[0] = 0
            self.direc[1] = (other.col - self.col)// abs(other.col - self.col)

        elif other.col == self.col and other.row != self.row:

            self.direc[0] = (other.row - self.row)// abs(other.row - self.row)
            self.direc[1] = 0

        if repr(other) == "White King":

            if self.direc == [1,0] or self.direc == [-1,0]:
                if self.col == other.col:

                    for row in range(self.row + self.direc[0], other.row, self.direc[0]):
                        if data.board[row][other.col] == True:
                            return False

                    return True

            if self.direc == [0,1] or self.direc == [0,-1]:
                if self.row == other.row:

                    for col in range(self.col + self.direc[1], other.col, self.direc[1]):
                        if data.board[self.row][col] == True:
                            return False
                    return True

    

    def allowMove(self, data, newRow, newCol):

        if data.inBlackCheck == False:


            if newRow == self.row and newCol != self.col:

                self.direc[0] = 0
                self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

            elif newCol == self.col and newRow != self.row:

                self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
                self.direc[1] = 0



            if self.direc == [0,1] or self.direc == [0,-1]:

                if self.row == newRow:
        
                    for col in range(self.col + self.direc[1], newCol + self.direc[1], self.direc[1]):
                        if data.board[self.row][col] == True:
                            return False

                    return True


       
            if self.direc == [1,0] or self.direc == [-1,0]:

                if self.col == newCol:

                    for row in range(self.row + self.direc[0], newRow + self.direc[0], self.direc[0]):          
                        if data.board[row][self.col] == True:
                            return False
                    
                    return True



    def move(self, data, newRow, newCol):

        if data.currPress != None:

            if (abs(newRow - self.row) <= 8 and self.col == newCol) or (abs(newCol - self.col) <= 8 and self.row == newRow):

                self.row = newRow
                self.col = newCol
                

                self.cx = data.margin + data.cellWidth//2 + data.cellWidth*self.col
                self.cy = data.margin + data.cellWidth//2 + data.cellWidth*self.row



    def attackHelper(self, data, newRow, newCol):


        if newRow == self.row and newCol != self.col:

            self.direc[0] = 0
            self.direc[1] = (newCol - self.col)// abs(newCol - self.col)

        elif newCol == self.col and newRow != self.row:

            self.direc[0] = (newRow - self.row)// abs(newRow - self.row)
            self.direc[1] = 0



        if self.direc == [0,1] or self.direc == [0,-1]:
    
            for col in range(self.col + self.direc[1], newCol, self.direc[1]):
                if data.board[self.row][col] == True:
                    return False

            return True


   
        if self.direc == [1,0] or self.direc == [-1,0]:

            for row in range(self.row + self.direc[0], newRow, self.direc[0]):          
                if data.board[row][self.col] == True:
                    return False
            
            return True



    def canAttack(self, data, newRow, newCol, other):

        if data.inBlackCheck == False:      
            if self.typ != other.typ and repr(other) != "White King":
                if other.row == newRow and other.col == newCol:
                    if self.attackHelper(data, newRow, newCol) == True:

                        return True
                    return False



    def draw(self, canvas):

        canvas.create_image(self.cx, self.cy, image = self.image)



from tkinter import *

####################################
# customize these functions
####################################  Animation framework from class notes 

def init(data):


    data.cellWidth = data.width//15
    data.margin = 175
    data.rows = 8
    data.cols = 8

    data.board = [[False for i in range(data.cols)] for j in range(data.rows)]

    data.inWhiteCheck = False
    data.inBlackCheck = False
    data.checkRow = None
    data.checkCol = None

    
    data.possibleButton = False

    
    data.lightRow = 0
    data.lightCol = 0

    data.prevKingRow = None
    data.prevKingCol = None

    data.selected = False

    data.prevPress = None

    data.currPress = None

    data.checkMate = False

    data.pawnFirstMove = False
    data.KingfirstMove = False

 
    data.initialPieces = []

    data.movePawn = []
    data.defeated = []

    data.possibleMoves = [ [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]

    data.whiteKing = WhiteKing(data.margin + 9/2 * data.cellWidth, data.margin + data.cellWidth//2)
    data.whiteQueen = WhiteQueen(data.margin + 7/2 * data.cellWidth, data.margin + data.cellWidth//2)

    data.whiteBishop1 = WhiteBishop(data.margin + 5/2 * data.cellWidth, data.margin + data.cellWidth//2, 2)
    data.whiteBishop2 = WhiteBishop(data.margin + 11/2 * data.cellWidth, data.margin + data.cellWidth//2, 5)

    data.whiteKnight1 = WhiteKnight(data.margin + 3/2 * data.cellWidth, data.margin + data.cellWidth//2, 1)
    data.whiteKnight2 = WhiteKnight(data.margin + 13/2 * data.cellWidth, data.margin + data.cellWidth//2, 6)

    data.whiteRook1 = WhiteRook(data.margin + 1/2 * data.cellWidth, data.margin + data.cellWidth//2, 0)
    data.whiteRook2 = WhiteRook(data.margin + 15/2 * data.cellWidth, data.margin + data.cellWidth//2, 7)


    data.blackKing = BlackKing(data.margin + 7/2 * data.cellWidth, data.margin + 15/2*data.cellWidth)
    data.blackQueen = BlackQueen(data.margin + 9/2 * data.cellWidth, data.margin + 15/2*data.cellWidth)

    data.blackBishop1 = BlackBishop(data.margin + 5/2 * data.cellWidth, data.margin + 15/2*data.cellWidth, 2)
    data.blackBishop2 = BlackBishop(data.margin + 11/2 * data.cellWidth, data.margin + 15/2*data.cellWidth, 5)

    data.blackKnight1 = BlackKnight(data.margin + 3/2 * data.cellWidth, data.margin + 15/2*data.cellWidth, 1)
    data.blackKnight2 = BlackKnight(data.margin + 13/2 * data.cellWidth, data.margin + 15/2*data.cellWidth, 6)

    data.blackRook1 = BlackRook(data.margin + 1/2 * data.cellWidth, data.margin + 15/2*data.cellWidth, 0)
    data.blackRook2 = BlackRook(data.margin + 15/2 * data.cellWidth, data.margin + 15/2*data.cellWidth, 7)

    data.checkMate = False


    data.initialPieces.append(data.whiteKing)
    data.initialPieces.append(data.whiteQueen)
    data.initialPieces.append(data.whiteBishop1)
    data.initialPieces.append(data.whiteBishop2)
    data.initialPieces.append(data.whiteKnight1)
    data.initialPieces.append(data.whiteKnight2)
    data.initialPieces.append(data.whiteRook1)
    data.initialPieces.append(data.whiteRook2)


    data.initialPieces.append(data.blackKing)
    data.initialPieces.append(data.blackQueen)
    data.initialPieces.append(data.blackBishop1)
    data.initialPieces.append(data.blackBishop2)
    data.initialPieces.append(data.blackKnight1)
    data.initialPieces.append(data.blackKnight2)
    data.initialPieces.append(data.blackRook1)
    data.initialPieces.append(data.blackRook2)



    for row in range(1,2):
        for col in range(data.cols):

            data.pawn = WhitePawn(data.margin + data.cellWidth//2 + col * data.cellWidth, data.margin + data.cellWidth//2 + (row + 1) * data.cellWidth//2, col)
            data.initialPieces.append(data.pawn)

    for row in range(6,7):
        for col in range(data.cols):

            data.pawn = BlackPawn(data.margin + data.cellWidth//2 + col * data.cellWidth, data.margin + data.cellWidth//2 + row * data.cellWidth, col)
            data.initialPieces.append(data.pawn)


    for row in range(0,2):
        for col in range(data.cols):
            data.board[row][col] = True

    for row in range(6,8):
        for col in range(data.cols):
            data.board[row][col] = True




def drawCell(canvas, data, row, col, color):

    x0, y0, x1, y1 = getBounds(data, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color)



def drawChessboard(canvas, data):

        for row in range(data.rows):
            for col in range(data.cols):

                if (row % 2 == 0 and col %2 == 0) or (row % 2 != 0 and col % 2 != 0):

                    drawCell(canvas, data, row, col, "burlywood")
                    
                else:
                    drawCell(canvas, data, row, col, "gray21")

                

def getBounds(data, row, col):


    x0 = data.margin + col * data.cellWidth
    y0 = data.margin + row * data.cellWidth
    x1 = data.margin + (col+1) * data.cellWidth
    y1 = data.margin + (row+1) * data.cellWidth

    return x0, y0, x1, y1





def isLegalPress(data, row, col, pawn):

    x0, y0, x1, y1 = getBounds(data, row, col)
    if pawn.cx not in range(x0, x1 + 1) or pawn.cy not in range(y0, y1 + 1):
        return False

    return True



def isLegalSecondPress(data, row, col, pawn):

    x0, y0, x1, y1 = getBounds(data, row, col)
    if pawn.cx < x0 or pawn.cx > x1 or pawn.cy < y0 or pawn.cy > y1:
        return True

    else:
        return False



def drawSelected(canvas, data, row, col):

    x0, y0, x1, y1 = getBounds(data, row, col)
    if data.selected == False:

        canvas.create_rectangle(x0, y0, x1, y1, outline = "red", width = "5")

    else:

        canvas.create_rectangle(x0, y0, x1, y1, outline = "green", width = "5")

def drawCheck(canvas, data, row, col):

    x0, y0, x1, y1 = getBounds(data, row, col)
    if data.inWhiteCheck == True or data.inBlackCheck == True:

        canvas.create_rectangle(x0,y0,x1,y1, fill = "yellow")


def drawCheckMate(canvas, data):

    if data.checkMate == True:
        canvas.create_rectangle(data.width//2 - data.margin, data.height//2 - data.margin, data.width//2 + data.margin, data.height//2 + data.margin, fill = "cyan")
        canvas.create_text(data.width//2, data.height//2, text = "Checkmate!")




def drawPossibleMoves(canvas, data, row, col):

    x0, y0, x1, y1 = getBounds(data, row, col)

    canvas.create_rectangle(x0,y0, x1, y1, fill ="light green")









def checkMate(data):


    for pawn in data.initialPieces:
        if repr(pawn) == "White King" or repr(pawn) == "Black King":
            checkCount = 0

            for move in data.possibleMoves:

                if pawn.row + move[0] >= 0 and pawn.row + move[0] <= 7 and pawn.col + move[1] >= 0 and pawn.col + move[1] <= 7:
                    if pawn.allowMove(data, pawn.row + move[0], pawn.col + move[1]) == True and data.board[pawn.row + move[0]][pawn.col + move[1]] == False:
                     
                        pawn.row += move[0]
                        pawn.col += move[1]

                        tempCount = 0

                        for other in data.initialPieces:
                            if repr(other) != "White King" and repr(other) != "Black King" and other.typ != pawn.typ:
                                if pawn.inCheck(data, other) == True and other.doCheck(data, pawn) == True:
                                    tempCount += 1
            
                        if tempCount == 0:

                            pawn.row -= move[0]
                            pawn.col -= move[1]
                            return False

                        pawn.row -= move[0]
                        pawn.col -= move[1]

                        checkCount += tempCount

            if checkCount >= 1:

                return True


             

def keyPressed(event, data):


    if event.keysym == "r":
        init(data)


    if data.checkMate == False:

        if event.keysym == "Up":
            if data.lightRow > 0:

                data.lightRow -= 1


        if event.keysym == "Down":
            if data.lightRow < data.rows - 1:
     
                data.lightRow += 1

            
        if event.keysym == "Left":

            if data.lightCol > 0:
                data.lightCol -= 1
       

        if event.keysym == "Right":

            if data.lightCol < data.cols - 1:
                data.lightCol += 1



        if event.keysym == "m":

            
            data.possibleButton = not data.possibleButton
            if data.possibleButton == True:

                for piece in data.initialPieces:

                    piece.possibleMoveLst = []
                

                    if piece.row == data.lightRow and piece.col == data.lightCol:

                        for row in range(data.rows):
                            for col in range(data.cols):

                                if data.board[row][col] == False:

                                    piece.getPossibleMoves(data, row, col)

              
                                


        if event.keysym == "Return":

            if data.prevPress == None:

                for pawn in data.initialPieces:

                    if isLegalPress(data, data.lightRow, data.lightCol, pawn):

                        data.prevPress = data.lightRow, data.lightCol
                        
                        data.selected = not data.selected
                        data.movePawn.append(pawn)
                        
                        

            elif data.prevPress != None:
                for pawn in data.initialPieces:  
                    if pawn in data.movePawn:

                        if isLegalSecondPress(data, data.lightRow, data.lightCol, pawn) == True:
                            data.currPress = data.lightRow, data.lightCol

                            if data.board[data.currPress[0]][data.currPress[1]] == False:

                                data.prevKingRow = None
                                data.prevKingCol = None

                                if pawn.allowMove(data, data.currPress[0], data.currPress[1]) == True:

                                    pawn.move(data, data.currPress[0], data.currPress[1])

                                    data.possibleButton = False


                                    if checkMate(data) == True:
                                        data.checkMate = True
                                        
                                    if repr(pawn) == "White Pawn" or repr(pawn) == "Black Pawn":
                                        pawn.firstMove = False

                                    if repr(pawn) == "White King": 
                                        pawn.canCastle = False

                                    if repr(pawn) == "Black King":
                                        pawn.canCastle = False
                            
                                    data.prevKingRow = data.prevPress[0]
                                    data.prevKingCol = data.prevPress[1]


                                    data.board[data.currPress[0]][data.currPress[1]] = True
                                    
                                    
                                    if repr(pawn) != "White King" and repr(pawn) != "Black King": #moving non-King piece to put King in check

                                        for other in data.initialPieces:

                                            if repr(other) == "White King": 

                                                if pawn.doCheck(data, other) == True:
                                                    
                                                    data.inWhiteCheck = True
                                                    data.checkRow = other.row
                                                    data.checkCol = other.col

                                            

                                            if repr(other) == "Black King":

                                                if pawn.doCheck(data, other) == True:

                                                    data.inBlackCheck = True
                                                    data.checkRow = other.row
                                                    data.checkCol = other.col

                                            


                                    elif repr(pawn) == "White King" or repr(pawn) == "Black King": #moving King piece, might end up in check

                                        for other in data.initialPieces:     
                                            if repr(other) != "White King" and repr(other) != "Black King":
                                                if pawn.inCheck(data, other) == True:

                                                    pawn.move(data, data.prevKingRow, data.prevKingCol)
                                                    data.board[data.currPress[0]][data.currPress[1]] = False

                                                
                                    data.board[data.prevPress[0]][data.prevPress[1]] = False


                                elif pawn.allowMove(data, data.currPress[0], data.currPress[1]) == False:
                                    data.board[data.currPress[0]][data.currPress[1]] = False
                                    
                                        
                            if data.board[data.currPress[0]][data.currPress[1]] == True:

                                for other in data.initialPieces:

                                    if repr(pawn) == "White King" and repr(other) == "White Rook":
                                        if pawn.allowMove(data, data.currPress[0], data.currPress[1]) == True:

                                            pawn.move(data, data.currPress[0], data.currPress[1])
                                            pawn.canCastle = False

                                    if repr(pawn) == "Black King" and repr(other) == "Black Rook":
                                        if pawn.allowMove(data, data.currPress[0], data.currPress[1]) == True:

                                            pawn.move(data, data.currPress[0], data.currPress[1])
                                            pawn.canCastle = False


                                    if pawn.canAttack(data, data.currPress[0], data.currPress[1], other) == True:

                                        pawn.attack(data, data.currPress[0], data.currPress[1])
                                        
                                        other.cx = random.randint(data.margin + data.rows*data.cellWidth, data.width - data.margin//2)
                                        other.cy = random.randint(data.margin//2, data.height - data.margin//2)

                                        data.defeated.append(other)
                                        data.initialPieces.remove(other)

                                        data.board[data.prevPress[0]][data.prevPress[1]] = False


                                        if repr(pawn) != "White King" and repr(pawn) != "Black King": #moving around non-king piece, puts king in check by attack another piece

                                            for other in data.initialPieces:
                                                if repr(other) == "White King":
                                                    if pawn.doCheck(data, other) == True:

                                                        data.inWhiteCheck = True
                                                        data.checkRow = other.row
                                                        data.checkCol = other.col

                                                if repr(other) == "Black King":
                                                    if pawn.doCheck(data, other) == True:

                                                        data.inBlackCheck = True
                                                        data.checkRow = other.row
                                                        data.checkCol = other.col

                                                        
                                        elif repr(pawn) == "White King" or repr(pawn) == "Black King": #moving around King, ends up in check by attacking another piece

                                            for other in data.initialPieces:

                                                if repr(other) != "White King" and repr(other) != "Black King":
                                                    if pawn.inCheck(data, other) == True:

                                                        data.checkRow = pawn.row
                                                        data.checkCol = pawn.col

                                                        

                            data.prevPress = None
                            data.currPress = None
                            
                            data.movePawn = []   
                            data.selected = not data.selected





def redrawAll(canvas, data):


    drawChessboard(canvas, data)

    for piece in data.initialPieces:

        if piece.row == data.lightRow and piece.col == data.lightCol and data.possibleButton == True:

            for elem in piece.possibleMoveLst:
                

                drawPossibleMoves(canvas, data, elem[0], elem[1])

    

    for row in range(data.rows):
        for col in range(data.cols):
            if (row,col) == (data.checkRow, data.checkCol) and data.checkRow != None and data.checkCol != None  and (data.inWhiteCheck == True or data.inBlackCheck == True):
                drawCheck(canvas, data, row, col)

    drawSelected(canvas, data, data.lightRow, data.lightCol)

    for pawn in data.initialPieces:
        pawn.draw(canvas)

    for killed in data.defeated:
        killed.draw(canvas)

    drawCheckMate(canvas, data)




def mousePressed(event, data):
    pass

    

def timerFired(data):
    pass


####################################
# use the run function as-is
####################################    #Run-function is from class notes

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 1000)