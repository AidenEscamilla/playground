def create_staircase(nums):
  step = 1
  subsets = []
  while len(nums) != 0:
    if len(nums) >= step:
      subsets.append(nums[0:step])
      nums = nums[step:]
      step += 1
    else:
      return False
      
  return subsets

f = open("secret_message.txt", "r")
words = {}

for line in f:
    tokens = line.split()             # Time: O(n) Space: O(n)
    words[int(tokens[0])] = tokens[1] # words[1] = 'hello'

f.close()

words = sorted(words.items())     # Time: O(n) Space: O(n)
words = [x[1] for x in words]     # Get the words in order
                                  # Time: O(n)

pyramid = create_staircase(words) # Time: O(n) Space: O(n)
result = ""

for subset in pyramid:
  result += subset[-1] + " "      # Time: O(n)

print(result.strip())