# Copy over your a1_partc.py file here
#    Main Author(s): MOHAMMED ZAID SHABBIR KHAN HAKIM
#    Main Reviewer(s): MOHAMMED ZAID SHABBIR KHAN HAKIM


class Stack:
	def __init__(self, cap=10):
		# Pre-allocate space for stack elements
		self.stack = [None] * cap  
		# Maximum capacity of the stack
		self.cap = cap  
		# The 'top' variable indicates the last item's index (-1 means the stack is empty)
		self.top = -1  

	def capacity(self):
		# Return the current capacity of the stack
		return self.cap

	def push(self, data):
		# Check if the stack is full and needs resizing
		if self.top + 1 == self.cap: 
			# Double the capacity
			self.cap *= 2
			# Create a new stack with the updated capacity
			new_stack = [None] * self.cap
			# Copy elements to the new stack
			for i in range(self.top + 1):
				new_stack[i] = self.stack[i]
			# Replace the old stack with the new one	
			self.stack = new_stack
		# Move the top pointer up by one position
		self.top += 1
		# Insert the new item at the top position
		self.stack[self.top] = data

	def pop(self):
		# Remove and return the top element of the stack if it's not empty
		if not self.is_empty():
			# Retrieve the top item
			data = self.stack[self.top]
			self.stack[self.top] = None  # Clear the reference
			# Move the top pointer down by one position
			self.top -= 1
			# Return the removed item
			return data
		else:
			# Raise an error if the stack is empty
			raise IndexError('pop() used on empty stack')

	def get_top(self):
		# Return the top element of the stack without removing it if it's not empty
		if not self.is_empty():
			# Return the top item
			return self.stack[self.top]
		else:
			# Return None if the stack is empty
			return None

	def is_empty(self):
		# Return True if top is -1, indicating no items are in the stack
		return self.top == -1

	def __len__(self):
		# The number of items is the top index + 1 (since index starts at 0)
		return self.top + 1


class Queue:

	def __init__(self, cap=10):
		# Initialize an array with 'cap' elements, all set to None.
		# Pre-allocate space for queue elements
		self.queue = [None] * cap 
		# Maximum capacity of the queue
		self.cap = cap  
		# Initialize 'front' to 0, indicating the position of the first element in the queue.
		self.front = 0  
		# Initialize 'size' to 0, indicating the queue is initially empty
		self.size = 0 

	def capacity(self):
		# Return the current capacity of the queue
		return self.cap

	def enqueue(self, data):
		# Check if the queue is full by comparing the current size with the maximum capacity
		if self.size == self.cap: 
			# Double the capacity
			new_cap = self.cap * 2
			# Create a new list with the updated capacity, all elements initialized to None
			new_queue = [None] * new_cap
			# Copy elements from the old queue to the new queue,
			# starting from 'front' and wrapping around as necessary to maintain the order
			for i in range(self.size):
				new_queue[i] = self.queue[(self.front + i) % self.cap]
			# Replace the old queue with the new, larger queue	
			self.queue = new_queue
			# Update the queue's capacity to reflect the new, larger size
			self.cap = new_cap
			# Reset front to 0 after resizing
			self.front = 0  

		# Calculate the index for the new element to be added at the back of the queue
		back = (self.front + self.size) % self.cap
		# Insert the new data at the calculated back position
		self.queue[back] = data
		# Increment the size of the queue to reflect the addition of the new element
		self.size += 1

	def dequeue(self):
		# If the queue is empty, raise an error
		if self.is_empty():
			raise IndexError('dequeue() used on empty queue')
		# Retrieve the value at the front of the queue
		front_value = self.queue[self.front]
		# Clear the reference at the front
		self.queue[self.front] = None
		# Move the front index to the next element, wrapping around as necessary
		self.front = (self.front + 1) % self.cap
		# Decrease the size of the queue since an element has been removed
		self.size -= 1
		# Return the dequeued element
		return front_value

	def get_front(self):
		# If the queue is empty, return None
		if self.is_empty():
			return None
		 # Return the value at the front of the queue without removing it
		return self.queue[self.front]

	def is_empty(self):
		# Return True if the queue is empty (size is 0), otherwise False
		return self.size == 0 

	def __len__(self):
		# Return the current number of elements in the queue
		return self.size



class Deque:

	def __init__(self, cap=10):
		# Initialize the deque with a fixed capacity and pre-allocate spac
		self.deque = [None] * cap
		# Maximum capacity of the Deque
		self.cap = cap
		# Initialize 'front' to 0, indicating the position of the first element in the Deque
		self.front = 0
		# Initialize 'size' to 0, indicating the Deque is initially empty
		self.size = 0

	def capacity(self):
		# Return the current capacity of the deque
		return self.cap

	def resize(self):
		# Double the capacity of the deque and rearrange the elements
		new_cap = self.cap * 2
		# Create a new deque with the new capacity
		new_deque = [None] * new_cap
		# Copy elements to the new deque, adjusting for circular nature
		for i in range(self.size):
			new_deque[i] = self.deque[(self.front + i) % self.cap]
		# Replace old deque with new deque
		self.deque = new_deque
		# Update the capacity
		self.cap = new_cap
		# Reset front index to 0
		self.front = 0

	def push_front(self, data):
		# If the deque is full, resize it
		if self.size == self.cap:
			self.resize()
		# Decrement front index circularly
		self.front = (self.front - 1) % self.cap
		# Insert new data at the front
		self.deque[self.front] = data
		# Increment size of deque
		self.size += 1

	def push_back(self, data):
		# If the deque is full, resize it
		if self.size == self.cap:
			self.resize()
		# Calculate new back inde
		back = (self.front + self.size) % self.cap
		# Insert new data at the back
		self.deque[back] = data
		# Increment size of deque
		self.size += 1

	def pop_front(self):
		# If deque is empty, throw an error
		if self.is_empty():
			raise IndexError('pop_front() used on empty deque')
		# Get the front value	
		value = self.deque[self.front]
		# Remove the front element
		self.deque[self.front] = None 
		# Increment front index circularly
		self.front = (self.front + 1) % self.cap
		# Decrement size of deque
		self.size -= 1
		# Return the removed value
		return value

	def pop_back(self):
		# If deque is empty, throw an error
		if self.is_empty():
			raise IndexError('pop_back() used on empty deque')
		# Calculate back index
		back_index = (self.front + self.size - 1) % self.cap
		# Get the back value
		value = self.deque[back_index]
		# Remove the back element
		self.deque[back_index] = None
		# Decrement size of deque
		self.size -= 1
		# Return the removed value
		return value

	def get_front(self):
		# If deque is empty, return None
		if self.is_empty():
			return None
		# Return the front value without removing it
		return self.deque[self.front]

	def get_back(self):
		# If deque is empty, return None
		if self.is_empty():
			return None
		# Calculate back index
		back_index = (self.front + self.size - 1) % self.cap
		# Return the back value without removing it
		return self.deque[back_index]

	def is_empty(self):
		# Return True if deque is empty, otherwise False
		return self.size == 0

	def __len__(self):
		# Return the number of elements in the deque
		return self.size

	def __getitem__(self, k):
        	# Return the k'th item from the front of the deque, without removing it
		# If index is out of bounds, raise an error
		if k < 0 or k >= self.size:
			raise IndexError('Index out of range')
		# Return the k-th item from the front
		return self.deque[(self.front + k) % self.cap]
