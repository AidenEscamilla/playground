'''
Credit: Code from geeksforgeeks.com-https://www.geeksforgeeks.org/dining-philosopher-problem-using-semaphores/
'''
import threading
import time
import random
import sys

# Define the number of philosophers and forks
num_philosophers = 5
num_forks = num_philosophers

# Define semaphores for the forks and the mutex
forks = [threading.Semaphore(1) for i in range(num_forks)]
mutex = threading.Semaphore(1)

# Define the philosopher thread function
def philosopher(index):
    has_not_eaten = True
    while has_not_eaten:
        print(f"Philosopher {index} is thinking...")
        time.sleep(random.randint(1, 5))  # Randomly think for 1-4 seconds
        
        mutex.acquire()                   # ???

        left_fork_index = index
        right_fork_index = (index + 1) % num_forks
        
        forks[left_fork_index].acquire()  # try and grab left fork
        forks[right_fork_index].acquire() # tray and grab right fork
        
        mutex.release()                   # ???
        
        print(f"Philosopher {index} is eating...")
        time.sleep(random.randint(1, 5))  # Randomly eat for 1-4 seconds
        
        forks[left_fork_index].release()  # Put left fork back on table
        forks[right_fork_index].release() # Put left fork back on table

        has_not_eaten = False # End philosopher


# Define the philosopher thread function w/ comments & better printing
def solution_philosopher(index):
    has_not_eaten = True
    while has_not_eaten:
        print(f"Philosopher {index} is thinking...")
        time.sleep(random.randint(1, 5))  # Randomly think for 1-4 seconds
        
        mutex.acquire()                   # Grab the "waiters attention" in order to grab forks
        print(f"Philosopher {index}: Hey waiter!")

        left_fork_index = index
        right_fork_index = (index + 1) % num_forks
        
        forks[left_fork_index].acquire()  # try and grab left fork
        forks[right_fork_index].acquire() # tray and grab right fork
        
        mutex.release()                   # Release the waiter
        
        print(f"Philosopher {index} is eating...")
        time.sleep(random.randint(1, 5))  # Randomly eat for 1-4 seconds
        
        print(f"Philosopher {index} is putting the forks down")
        forks[left_fork_index].release()  # Put left fork back on table
        forks[right_fork_index].release() # Put left fork back on table

        print(f"Philosopher {index} is done :)")
        has_not_eaten = False # End philosopher

# Create a thread for each philosopher
philosopher_threads = []
if len(sys.argv) <= 1:
  for i in range(num_philosophers):
    philosopher_threads.append(threading.Thread(target=philosopher, args=(i,)))
elif sys.argv[1] == "--solution":
  for i in range(num_philosophers):
    philosopher_threads.append(threading.Thread(target=solution_philosopher, args=(i,)))

    
# Start the philosopher threads
for thread in philosopher_threads:
    thread.start()
    
# Wait for the philosopher threads to complete
for thread in philosopher_threads:
    thread.join()