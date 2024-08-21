# Main Author(s): Usman Ali
# Main Reviewer(s): Mohammed Zaid Shabbir Khan Hakim

class HashTable:
    # You cannot change the function prototypes below.
    # How you implement the class is your choice as long as it is a hash table.
    
    def __init__(self, cap=32):
        """
        Initialize the hash table with a given capacity.
        
        Parameters:
        cap (int): The initial capacity of the hash table. Defaults to 32.
        
        Initializes:
        self.table: A list of size `cap` initialized with None values.
        self.capacity_value: The capacity of the hash table.
        self.size: The number of elements currently in the table.
        """
        self.capacity_value = cap
        self.table = [None] * self.capacity_value
        self.size = 0

    def insert(self, key, value):
        """
        Insert a key-value pair into the hash table.
        
        Parameters:
        key: The key to be inserted into the hash table.
        value: The value associated with the key.
        
        Returns:
        bool: Returns True if the key-value pair was successfully added.
              Returns False if the key already exists in the table.
        
        Description:
        This function uses linear probing to resolve collisions.
        If the load factor exceeds 0.7, the table is resized, and all elements are rehashed.
        """
        # Find the position to insert the new key
        idx = hash(key) % self.capacity_value
        while self.table[idx]:
            if self.table[idx][0] == key:
                return False  # Key already exists, do not insert
            idx = (idx + 1) % self.capacity_value
        self.table[idx] = (key, value)
        self.size += 1
        
        # Check if load factor exceeded for resizing
        if self.size / self.capacity_value > 0.7:
            old_table = self.table
            self.capacity_value *= 2
            self.table = [None] * self.capacity_value
            self.size = 0

            # Rehash all existing items
            for item in old_table:
                if item:
                    idx = hash(item[0]) % self.capacity_value

                    # Linear probing
                    while self.table[idx]:
                        idx = (idx + 1) % self.capacity_value
                    self.table[idx] = item
                    self.size += 1
        return True

    def modify(self, key, value):
        """
        Modify the value associated with a given key in the hash table.
        
        Parameters:
        key: The key whose value needs to be modified.
        value: The new value to associate with the key.
        
        Returns:
        bool: Returns True if the value was successfully modified.
              Returns False if the key does not exist in the table.
        
        Description:
        This function searches for the key and updates its value if found.
        Uses linear probing to handle collisions during search.
        """
        idx = hash(key) % self.capacity_value
        while self.table[idx]:
            if self.table[idx][0] == key:
                self.table[idx] = (key, value)
                return True
            idx = (idx + 1) % self.capacity_value
        return False

    def remove(self, key):
        """
        Remove a key-value pair from the hash table.
        
        Parameters:
        key: The key to be removed from the hash table.
        
        Returns:
        bool: Returns True if the key-value pair was successfully removed.
              Returns False if the key does not exist in the table.
        
        Description:
        This function removes the element associated with the key.
        After removal, it handles rehashing of subsequent elements to maintain the hash table's integrity.
        """
        idx = hash(key) % self.capacity_value
        for _ in range(self.size):
            if self.table[idx] and self.table[idx][0] == key:
                self.table[idx] = None
                self.size -= 1

                # Check for swapping with new empty spot
                next_idx = (idx + 1) % self.capacity_value
                while self.table[next_idx]:
                    rehash_idx = hash(self.table[next_idx][0]) % self.capacity_value
                    if rehash_idx <= idx:
                        self.table[idx] = self.table[next_idx]
                        self.table[next_idx] = None
                        idx = next_idx
                    next_idx = (next_idx + 1) % self.capacity_value
                return True
            
            idx = (idx + 1) % self.capacity_value
        return False
   
    def search(self, key):
        """
        Search for a value associated with a given key in the hash table.
        
        Parameters:
        key: The key to search for in the hash table.
        
        Returns:
        The value associated with the key if found, otherwise None.
        
        Description:
        This function searches for the key using linear probing to resolve collisions.
        If the key is found, it returns the associated value.
        """
        idx = hash(key) % self.capacity_value
        while self.table[idx]:
            if self.table[idx][0] == key:
                return self.table[idx][1]
            idx = (idx + 1) % self.capacity_value
        return None

    def capacity(self):
        """
        Get the current capacity of the hash table.
        
        Returns:
        int: The number of spots available in the hash table.
        """
        return self.capacity_value

    def __len__(self):
        """
        Get the current number of elements in the hash table.
        
        Returns:
        int: The number of records currently stored in the table.
        """
        return self.size
