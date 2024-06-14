import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")
    #returns true if is mine and false otherwise
    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if len(self.cells) == self.count:
            mines = self.cells
            print(f'Known mines: {mines}')
        return mines
    

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes =set()
        if self.count == 0:
            safes = self.cells
            print(f'Known safes: {safes}')
        return safes
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -=1
    
            
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            print(f'Cell: {cell} Marked as Safe')


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        #2) mark the cell as safe
        self.mark_safe(cell)
        #3) add a new sentence to the AI's knowledge base
        #       based on the value of `cell` and `count`
        neighbor_cells = set()
          # Loop over all cells within one row and column
        
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update neighbors
                if 0 <= i < self.height and 0 <= j < self.width:
                    new_neighbor_cell = (i,j)
                    if new_neighbor_cell in self.safes:
                        continue
                    elif new_neighbor_cell in self.mines:
                        count -= 1
                    else:
                        neighbor_cells.add(new_neighbor_cell)
        if len(neighbor_cells) == count:
            for neighbor_cell in neighbor_cells:
                self.mark_mine(neighbor_cell)
        elif count == 0 and len(neighbor_cells)>0:
            for neighbor_cell in neighbor_cells:
                self.mark_safe(neighbor_cell)
        else:
            new_sentence = Sentence(neighbor_cells,count)
            self.knowledge.append(new_sentence)

        #4) mark any additional cells as safe or as mines
        #       if it can be concluded based on the AI's knowledge base
        discovered_mines = set()
        discovered_safes = set() 
        for sentence in self.knowledge:
            discovered_mines.update(sentence.known_mines())
            discovered_safes.update(sentence.known_safes())
        for discovered_mine in discovered_mines:
            self.mark_mine(discovered_mine)

        for discovered_safe in discovered_safes:
            self.mark_safe(discovered_safe)

        #5) add any new sentences to the AI's knowledge base
        #       if they can be inferred from existing knowledge
        new_knowledge = []
        cells_to_mark_as_safe = []
        cells_to_mark_as_mines = []
        for sentenceA in self.knowledge:
            for sentenceB in self.knowledge:
                if sentenceA == sentenceB:
                    continue
                elif sentenceA.cells.issubset(sentenceB.cells):
                    print(f'{sentenceA} is subset of {sentenceB}')
                    new_cells_for_new_sentence = sentenceB.cells - sentenceA.cells
                    new_count = sentenceB.count - sentenceA.count
                    new_sentence = Sentence(new_cells_for_new_sentence, new_count)
                    print(f'New Sentence: {new_sentence} ')
                    if new_sentence.count == 0:
                        for cell in new_sentence.cells:
                            cells_to_mark_as_safe.append(cell)
                            #self.mark_safe(cell)
                    elif new_sentence.count == len(new_sentence.cells):
                        for cell in new_sentence.cells:
                            #self.mark_mine(cell)
                            cells_to_mark_as_mines.append(cell)
                    else:
                        new_knowledge.append(new_sentence)

        self.knowledge.extend(new_knowledge)
        for cell_to_mark_as_mine in cells_to_mark_as_mines:
            self.mark_mine(cell_to_mark_as_mine)
        for cell_to_mark_as_safe in cells_to_mark_as_safe:
            self.mark_safe(cell_to_mark_as_safe)

        print('Sentences:')
        for sentence in self.knowledge:
            print(sentence)
        print('Safe Moves(Withot the safe moves i already played)')
        for move in self.safes - self.moves_made:
            print(move)
        print('Mines Detected')
        for mine in self.mines:
            print(mine)

                
            


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        """ for safe_move in self.safes:
            if safe_move not in self.moves_made and safe_move not in self.mines:
                return safe_move
            else:
                return None """
        possible_moves = [move for move in self.safes if move not in self.moves_made and move not in self.mines]
    
        if possible_moves:
            return random.choice(possible_moves)
        else:
            return None
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            random_cell = (i, j)
            if random_cell not in self.mines and random_cell not in self.moves_made:
                return random_cell
            else: return None
            # Continue looping if the random cell is either a mine or already chosen

               
