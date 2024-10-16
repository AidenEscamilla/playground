import random
import numpy as np

class Player:
  def __init__(self, name, ship_array):
    self.name = name
    self.board = [ [0] * 10 for _ in range(10)]
    self.ships_left = 5
    self.ships = ship_array

  def get_board(self):
    return self.board
  
  def set_board(self, new_board):
    self.board = new_board
  
  def get_ships_left(self):
    return self.ships_left
  
  def get_ships_array(self):
    return self.ships
  
  def sink_ship(self): #Sunken ship = -1 ships_left
    self.ships_left -= 1

  def is_loser(self):
    return self.ships_left == 0
  
  def print_board(self):
    print(f"\n#################### {self.name}  ######################")
    print("  |_A_||_B_||_C_||_D_||_E_||_F_||_G_||_H_||_I_||_J_|")
    for row_num in range(len(self.board)):
      row = f"{row_num}."
      for col in self.board[row_num]:
        if col == -1: # miss
          row += "|_x_|"
        elif col == 1: # hit
          row += "|hit|"
        else: # must be 0 or hidden ship
          row += "|___|"
      print(row)

  def print_ship_board(self):
    print(f"\n#################### {self.name}  ######################")
    print("  |_A_||_B_||_C_||_D_||_E_||_F_||_G_||_H_||_I_||_J_|")
    for row_num in range(len(self.board)):
      row = f"{row_num}."
      for col in self.board[row_num]:
        if col == -1: # miss
          row += "|_x_|"
        elif col == 1: # hit
          row += "|hit|"
        elif col >= 10: # double digit = ship
          row += "|_s_|"
        else:
          row += "|___|"
      print(row)
  
  def is_coord_unguessed(self, coord_string_list):
    column = {'a': 0, 'b': 1, 'c': 2,
              'd': 3, 'e': 4, 'f': 5,
              'g': 6, 'h': 7, 'i': 8, 'j': 9,}
    col_index = column[coord_string_list[0].lower()] # Map letter to col index
    row_index = int(coord_string_list[1]) # input function checks for isdigit

    if self.board[row_index][col_index] == 0: # 0 = is unguessed
      return True
    elif self.board[row_index][col_index] >=10: # Ship here & unguessed
      return True
    else: # -1 or 1 = is guessed
      return False
    
  def add_shot_to_board(self, coord_string):
    coord_string_list = list(coord_string)
    column = {'a': 0, 'b': 1, 'c': 2,
              'd': 3, 'e': 4, 'f': 5,
              'g': 6, 'h': 7, 'i': 8, 'j': 9,}
    col_index = column[coord_string_list[0].lower()] # Map letter to col index
    row_index = int(coord_string_list[1]) # input function checks for isdigit
    # Come back here and check if there's a ship here
    board_value = self.board[row_index][col_index]
    if board_value == 0: # If nothing there
      self.board[row_index][col_index] = -1 # add miss to board
    elif board_value >= 10: # if a ship
      self.board[row_index][col_index] = 1  # add hit to board
      
      ships = self.get_ships_array()

      for ship in ships:  # Add hit to the ship
        if board_value == ship.get_id(): # find the matching ship
          ship.hit() # ship loses 1 health
          if ship.is_sunk():
            self.ships_left -= 1 # lose 1 ship to player.ships_left
            if self.name == "Enemy":
              print(f"You sunk my {ship.get_name()}") 
            else:
              print(f"I sunk your {ship.get_name()} >:)")
          break # Don't check other ships if you found the right one

  def add_ship_to_board(self, ship):
    # get orientation
    orientation = input(f"Do you want your {ship.get_name()}({ship.get_length()}) vertical or horizontal? (v, h): ").lower()

    while orientation not in ['h', 'v']: # validate input
      print("invalid. Please type = \'h\' or \'v\'")
      orientation = input(f"Do you want your {ship.get_name()} vertical or horizontal? (v, h): ").lower()
    ship.set_orientation(orientation)

    self.print_ship_board()
    ship_front = input("Type a coordinate for the start of the ship (\'B9\'): ").upper() # get starting x,y
    while not is_valid_coord(self, ship_front): # validate input
      print("invalid. Please type a coord like: C4")
      self.print_ship_board()
      ship_front = input("Type a coordinate for the start of the ship (\'B9\'): ").upper() # get starting x,y
    
    ship_back_options = get_ship_back_options(self, orientation.lower(), ship_front, ship.get_length() - 1) # get options

    # get other end of ship coords
    ship_back = input(f"Type a coordinate for the back of the ship. Your options are {ship_back_options}: ").upper()
    while ship_back.upper() not in ship_back_options:# validate input
      print("invalid. Select one of the options")
      ship_back = input(f"Type a coordinate for the back of the ship. Your options are {ship_back_options}: ").upper()
    
    if self.no_overlapping_ships(ship, ship_front, ship_back): # if there's no 'stacking' cheat
      self.put_ship_values_on_board(ship)
    else: #recursive try again
      self.add_ship_to_board(ship)

  def add_ship_to_computer_board(self, ship):
    # get orientation
    orientation = random.choice(['h', 'v'])
    ship.set_orientation(orientation)

    board = np.array(self.get_board())

    ship_indicies = board >= 10
    unguessed_indicies = board == 0
    # Get the indices where the array is True
    true_indices = np.argwhere(ship_indicies | unguessed_indicies)
    # Choose a random index from the list of True indices
    random_index = np.random.choice(true_indices.shape[0])
    # Get the row and column of the chosen index
    row, col = true_indices[random_index]
    index_to_column = {0: 'A', 1: 'B',  2: 'C',
            3: 'D',  4: 'E',  5: 'F',
            6: 'G',  7: 'H',  8: 'I',  9: 'J'}
    random_coord = ''.join([index_to_column[row],str(col)])

    ship_front = random_coord
    
    ship_back_options = get_ship_back_options(self, orientation.lower(), ship_front, ship.get_length() - 1) # get options
    if len(ship_back_options) == 0: #incase there's no valid options
      self.add_ship_to_computer_board(ship) # recursive retry
      return None # DONT DO ANYTHING BELOW, leave function if lower recursive call passes
    # get other end of ship coords
    ship_back = random.choice(ship_back_options)

    if self.no_overlapping_ships(ship, ship_front, ship_back): # if there's no 'stacking' cheat
      self.put_ship_values_on_board(ship)
    else: #recursive try again
      self.add_ship_to_computer_board(ship)

  def no_overlapping_ships(self, ship, coord1, coord2):
    orientation = ship.get_orientation()
    ship_coords = []
    start_coord = None
    end_coord = None

    # Assign start & end
    if coord1 < coord2: #horz = 'A4' < 'E4' OR vert = 'E0' < 'E4'
      start_coord = coord1
      end_coord = coord2
    else: #otherwise, swap them
      start_coord = coord2
      end_coord = coord1

    ship_coords.append(start_coord) # add start
    temp = list(start_coord)
    while ''.join(temp) != end_coord: # add all in between coords
      if orientation == 'h':
        temp[0] = chr(ord(temp[0]) + 1) # +1 horz letter
      else:
        temp[1] = str(int(temp[1]) + 1) # +1 vert number

      ship_coords.append(''.join(temp)) # add coord to list

    ship.set_coords(ship_coords) # add the coords to ship object

    for coord in ship_coords:
      coord_string_list = list(coord)
      column = {'a': 0, 'b': 1, 'c': 2,
                'd': 3, 'e': 4, 'f': 5,
                'g': 6, 'h': 7, 'i': 8, 'j': 9,}
      col_index = column[coord_string_list[0].lower()] # Map letter to col index
      row_index = int(coord_string_list[1]) # input function checks for isdigit

      if self.board[row_index][col_index] >= 10: # if coord has a ship on it already
        print("Arrrrg ya dirty cheater. No stackin' ships! Try again\n")
        return False
    
    return True

  def put_ship_values_on_board(self, ship):
    for coord in ship.get_coords():
      coord_char_list = list(coord)
      column = {'a': 0, 'b': 1, 'c': 2,
                'd': 3, 'e': 4, 'f': 5,
                'g': 6, 'h': 7, 'i': 8, 'j': 9,}
      col_index = column[coord_char_list[0].lower()] # Map letter to col index
      row_index = int(coord_char_list[1]) # input function checks for isdigit

      self.board[row_index][col_index] = ship.get_id()  


def get_ship_back_options(player, orientation_char, ship_starting_coord, ship_length):
  coord_list = list(ship_starting_coord)
  options = []

  if orientation_char == 'h':
    temp1 = coord_list.copy()
    temp2 = coord_list.copy()

    temp1[0] = chr(ord(coord_list[0]) + ship_length) # move right
    if is_valid_coord(player, ''.join(temp1)):
      options.append(''.join(temp1).upper()) # append valid coord

    temp2[0] = chr(ord(coord_list[0]) - ship_length) # move left
    if is_valid_coord(player, ''.join(temp2)):
      options.append(''.join(temp2).upper()) # append valid coord

  elif orientation_char == 'v': 
    temp1 = coord_list.copy()
    temp2 = coord_list.copy()

    temp1[1] = str(int(coord_list[1]) + ship_length) # Move 'down' (toward 9)
    if is_valid_coord(player, ''.join(temp1)):
      options.append(''.join(temp1).upper()) # append valid coord
    
    temp2[1] = str(int(coord_list[1]) - ship_length) # Move 'up' (toward 0)
    if is_valid_coord(player, ''.join(temp2)):
      options.append(''.join(temp2).upper()) # append valid coord

  return options

def is_valid_coord(player, coord_string):
  coord_list = list(coord_string.lower())

  if len(coord_list) != 2: # Example: H11 is invalid even though char[1] == 1
    return False

  if not coord_list[1].isdigit(): # Guard against casting non-integers
    return False

  if coord_list[0] in ['a','b','c','d','e','f','g','h','i','j'] \
     and int(coord_list[1]) < 10: # if valid coord
     if  has_no_ship(player, coord_list): # And coord has no ship already
        return True
     else:  # Could left this fall to false
       return False
  
  return False

def has_no_ship(player, coord_list):
  board = player.get_board()
  column = {'a': 0, 'b': 1, 'c': 2,
          'd': 3, 'e': 4, 'f': 5,
          'g': 6, 'h': 7, 'i': 8, 'j': 9,}
  col_index = column[coord_list[0].lower()] # Map letter to col index
  row_index = int(coord_list[1]) # Comes in as isdigit from previous function

  board_value = board[row_index][col_index]
  if board_value >= 10:
    return False
  else:
    return True

class Ship:
  def __init__(self, name, id, length):
    self.name = name
    self.id = id
    self.length = length
    self.orientation = None
    self.coords = None
    self.health = length # a.k.a is_sunk tracker

  def set_orientation(self, orientation_string):
    self.orientation = orientation_string.lower()
  
  def set_coords(self, coords_list): # come back and make sure this is right
    self.coords = coords_list

  def get_name(self):
    return self.name
  
  def get_coords(self):
    return self.coords
  
  def get_length(self):
    return self.length

  def get_orientation(self):
    return self.orientation
  
  def get_id(self):
    return self.id
  
  def get_health(self):
    return self.health
  
  def hit(self): # Lose 1 health on hit
    self.health -= 1

  def is_sunk(self):
    return self.health <= 0 # If 0 health returns True, 
                            # else there's still an unhit section, returns False
  

def get_player_torpedo_input(enemy_computer):
  valid_input = False
  user_input = None
  valid_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
  valid_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

  while not valid_input:
    user_input = input("Type torpedo coordinate (\'A4\'): ")
    split_input = list(user_input)

    if len(split_input) < 2: # Not enough input
      print("Invalid coordinate, try again")
      continue #skip other checks & retry

    if not split_input[1].isdigit(): # If it's not a number
      print("Invalid coordinate, try again")
      continue #skip other checks & retry

    if (split_input[0].lower() in valid_letters) and \
       (int(split_input[1]) in valid_numbers):  # if valid coord
      if enemy_computer.is_coord_unguessed(split_input): # if not guessed before
        return user_input # Valid input breaks loop by returning
      else:
        print("Already guessed this coordinate, try again")
        continue
    else:
      print("Invalid coordinate, try again")
    
def get_computer_torpedo(player):
  index_to_column = {0: 'A', 1: 'B',  2: 'C',
            3: 'D',  4: 'E',  5: 'F',
            6: 'G',  7: 'H',  8: 'I',  9: 'J'}
  board = np.array(player.get_board())

  ship_indicies = board >= 10
  unguessed_indicies = board == 0
  # Get the indices where the array is True
  possible_indices = np.argwhere(ship_indicies | unguessed_indicies)
  # Choose a random index from the list of True indices
  random_index = np.random.choice(possible_indices.shape[0])
  # Get the row and column of the chosen index
  row, col = possible_indices[random_index]
  random_coord = ''.join([index_to_column[col], str(row)])

  return random_coord   


player_ships = [ Ship("Carrier", 10, 5), Ship("Battleship", 11, 4), 
          Ship("Cruiser", 12, 3), Ship("Submarine", 13, 3), 
          Ship("Patrol boat", 14, 2)
        ]

enemy_ships = [ Ship("Carrier", 10, 5), Ship("Battleship", 11, 4), 
          Ship("Cruiser", 12, 3), Ship("Submarine", 13, 3), 
          Ship("Patrol boat", 14, 2)
        ]

enemy = Player("Enemy", enemy_ships)
myself = Player("Player", player_ships)

game_over = False

# Add ships to each board
for ship in myself.get_ships_array():
  myself.add_ship_to_board(ship)

for ship in enemy.get_ships_array():
  enemy.add_ship_to_computer_board(ship)

# Gameplay loop
while not game_over:
  enemy.print_board()
  myself.print_board()
  print()
  player_shot = get_player_torpedo_input(enemy)  # Shoot enemy ship
  enemy.add_shot_to_board(player_shot)    # Add to top board

  enemy_shot = get_computer_torpedo(myself) # Computer shoots players ship
  myself.add_shot_to_board(enemy_shot)      # Add to bottom board
  

  if myself.is_loser():
    print("gg, better luck next time >:)")
    game_over = True
  elif enemy.is_loser():
    print("Congrats, you win!!\nGoodbye...")
    game_over = True

print("############## GAME OVER ##############")
enemy.print_board()
myself.print_board()

# Testing commit setup