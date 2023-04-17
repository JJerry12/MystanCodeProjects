"""
File: boggle.py
Name: Jerry
----------------------------------------
You have to find as many words as possible on the 4X4 grid.
You can follow from one letter to another if it is a neighbour (in all directions).
You cannot use a letter more than once in a word.
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'

# Global variable
dict_lst = []                # The list stores all the words from the dictionary


def main():
	"""
	This program plays the boggle game
	"""
	read_dictionary()

	start = time.time()
	####################
	while True:
		row_1 = input('1 row of letters: ')
		if not check_input(row_1):
			break
		row_2 = input('2 row of letters: ')
		if not check_input(row_2):
			break
		row_3 = input('3 row of letters: ')
		if not check_input(row_3):
			break
		row_4 = input('4 row of letters: ')
		if not check_input(row_4):
			break

		# a list stores the all letters user input (case-insensitive)
		letter_set = [row_1.lower().split(), row_2.lower().split(),
					  row_3.lower().split(), row_4.lower().split()]

		cur_list = []                         # the list that stores the present elements
		found_list = []                       # the list that stores the strings having been used
		total_list = []                       # the list that stores the all words having been found

		for i in range(len(letter_set)):               # Row
			for j in range(len(letter_set[i])):        # Col
				cur_list.clear()
				cur_list.append(letter_set[i][j])
				found_list.clear()
				found_list.append((i, j))
				find_anagrams(letter_set, cur_list, [i, j], found_list, total_list)
		print("There are " + str(len(total_list)) + " words in total.")

	####################
	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')


def find_anagrams(letter_set, cur_list, position_list, found_list, total_list):
	"""
	:param letter_set: a list stores the all letters user input
	:param cur_list: the list that stores the present elements
	:param position_list: the list that records the current location
	:param found_list: the list that stores the strings having been used
	:param total_list: the list that stores the all words having been found
	"""
	cur_s = ''.join(cur_list)
	if has_prefix(cur_s):

		# Recursive case
		# surrounding neighbors
		for i in range(position_list[0]-1, position_list[0]+2):
			for j in range(position_list[1]-1, position_list[1]+2):
				if 0 <= i < 4 and 0 <= j < 4:

					# can not move back to the starting letter
					if (i, j) is not (position_list[0], position_list[1]):

						# can not use the repeated letters
						if (i, j) not in found_list:
							found_list.append((i, j))

							# Choose
							cur_list.append(letter_set[i][j])

							if len(cur_list) >= 4:
								cur_s = ''.join(cur_list)
								if cur_s in dict_lst and cur_s not in total_list:
									print('Found' + ' \"' + cur_s + '\"')
									total_list.append(cur_s)

							# Explore
							find_anagrams(letter_set, cur_list, [i, j], found_list, total_list)

							# Un-choose
							found_list.pop()
							cur_list.pop()


def check_input(s):
	"""
	:param s: (str) The strings that user input
	:return: (bool) If the input strings meet the requirements
	"""
	if len(s.split()) != 4:
		print('Illegal input')
		return False
	for ele in s.split():
		if len(ele) != 1:
			print('Illegal input')
			return False
	return True


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	with open(FILE, "r") as f:
		for line in f:
			words = line.split()
			for word in words:
				if len(word) >= 4:           # find only words with length at least 4 letters
					dict_lst.append(word.strip())


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	for word in dict_lst:
		if word.startswith(sub_s):
			return True


if __name__ == '__main__':
	main()
