invalid_input = True

while invalid_input:
  side_length = input("How big should the square be?: ")
  
  if side_length.isdigit():
    side_length = int(side_length)
    invalid_input = False
  else:
    print("invalid. Try again")

# O(N) solution
# single_row = '* ' * side_length
# for length in range(side_length):
#   print(single_row)

# O(n^2) solution
for length in range(side_length): # O(n)
  row = ''
  for height in range(side_length): # O(n) INSIDE a O(n)
    row += '* '
  print(row)
