# copy over your a1_partd.py file here
#    Main Author(s): MOHAMMED ZAID SHABBIR KHAN HAKIM
#    Main Reviewer(s): MOHAMMED ZAID SHABBIR KHAN HAKIM

from a1_partc import Queue

def get_overflow_list(grid):
	overflow_list = []
	rol_len = len(grid)
	col_len = len(grid[0])

	# Use two for loop to check all the cell in the grid
	# If the cell is overflow, add it to the overflow_list
	for i in range(rol_len):
		for j in range(col_len):
			# Determine the number of neighbors
			neighbors = 4
			# Check if the cell is on the edge
			if i == 0 or i == rol_len - 1:
				neighbors -= 1
			# Check if the cell is on the edge
			if j == 0 or j == col_len - 1:
				neighbors -= 1

			# Check if the cell is overflow
			if abs(grid[i][j]) >= neighbors:
				overflow_list.append((i, j))

	return overflow_list if overflow_list else None



def overflow(grid, a_queue):
	overflow_list = get_overflow_list(grid)
	if overflow_list == None or check_all_same_sign(grid):
		return 0

	directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
	rol_len = len(grid)
	col_len = len(grid[0])

	# Increase 1 to all the neighbors of the overflow cells
	for cell in overflow_list:
		x, y = cell
		for dx, dy in directions:
			nx, ny = x + dx, y + dy
			if 0 <= nx < rol_len and 0 <= ny < col_len:
				increase_one_and_pass_sign(x, y, grid, nx, ny)

	# If two overflow cells are neighbors, they will become 1 or -1
	# Create a neighbor_list to store the neighbor cells
	# After setting two neighbor_list cell to 1 or -1, remove the duplicate element from the overflow_list
	neighbor_list = []
	for i in range(len(overflow_list)):
		for j in range(i+1, len(overflow_list)):
			if is_neighbor(overflow_list[i], overflow_list[j]):
				set_two_neighbor_overflow_cell(overflow_list[i], overflow_list[j], grid)
				neighbor_list.append(overflow_list[i])
				neighbor_list.append(overflow_list[j])

	# After setting two neighbor_list cell to 1 or -1
	# Remove the duplicate element from the overflow_list
	overflow_list = [cell for cell in overflow_list if cell not in neighbor_list]

	# The rest of the overflow cells will become 0
	for cell in overflow_list:
		x, y = cell
		grid[x][y] = 0

	# Add the grid to the queue by value NOT by reference
	new_grid = [row[:] for row in grid]
	a_queue.enqueue(new_grid)

	# Recursion
	return 1 + overflow(grid, a_queue)

def is_neighbor(cell1, cell2):
	x1, y1 = cell1
	x2, y2 = cell2
	return abs(x1 - x2) + abs(y1 - y2) == 1
	
# Plus one to the cell and pass the sign to the cell
def increase_one_and_pass_sign(overflow_row, overflow_col, grid, row, col):
	# Get absolute value of the cell and plus one
	grid[row][col] = abs(grid[row][col]) + 1
	
	# Pass the sign to the cell
	if grid[overflow_row][overflow_col] < 0:
		grid[row][col] = -grid[row][col]
	
# is_positive() function
def is_positive(self):
	return self >= 0

# Check the grid is all the same sign or not
def check_all_same_sign(grid):
	# Get the first not 0 cell and set it as the first sign
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] != 0:
				first_sign = is_positive(grid[i][j])	# True is positive, False is negative
				break
	# Check all the cell in the grid
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] != 0 and is_positive(grid[i][j]) != first_sign:
				return False
	return True

# Record two neighbor cell and set them to 1 or -1
def set_two_neighbor_overflow_cell(c1, c2, grid):
	# Get sign of the t1 and t2
	sign_t1 = is_positive(grid[c1[0]][c1[1]])
	sign_t2 = is_positive(grid[c2[0]][c2[1]])
	# Set the t1 and t2 to 1 or -1
	grid[c1[0]][c1[1]] = 1 if sign_t2 else -1
	grid[c2[0]][c2[1]] = 1 if sign_t1 else -1
