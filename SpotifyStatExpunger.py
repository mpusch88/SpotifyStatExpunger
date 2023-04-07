import json
import os
import re

# get the current working directory from the user
directory = input("\nEnter the directory path:\n")

# find number of files matching the pattern endsong_*.json in directory
num_files = len([f for f in os.listdir(directory) if re.match(r'endsong_.*\.json', f)])

if num_files > 0:
	print(f"\n  Number of endsong files in directory '{directory}': {num_files}\n")

	# get the string to search for from the user
	pattern = input("Enter the string to search for:\n")

	#convert the string to regular expression
	pattern = pattern.replace(" ", "\s")
	pattern = r'\{.*' + pattern + r'.*\}'

	print("\n Searching for the following regular expression: " + pattern + "\n")

	total_objects = 0

	for i in range(num_files):
		# Create the file name
		fileName = directory + "\endsong_" + str(i) + ".json"

		# Read the JSON data from the file
		with open(fileName, 'r', encoding='utf-8') as f:
			data = json.load(f)

		objects_to_delete = []

		# Traverse the object and identify the matching objects
		for obj in data:
			if re.match(pattern, json.dumps(obj), flags=re.IGNORECASE):
				objects_to_delete.append(obj)

		print(f"Number of objects to delete in file {fileName}: {len(objects_to_delete)}")
		total_objects += len(objects_to_delete)

	if total_objects > 0:

		#ask user whether they would like to force all updates
		force = input("\nDo you want to force all updates? (y/n): ")

		# Traverse through all the files in the directory
		for i in range(num_files):
			# Create the file name
			fileName = directory + "\endsong_" + str(i) + ".json"

			# Read the JSON data from the file
			with open(fileName, 'r', encoding='utf-8') as f:
				data = json.load(f)

			objects_to_delete = []

			# Traverse the object and identify the matching objects
			for obj in data:
				if re.match(pattern, json.dumps(obj), flags=re.IGNORECASE):
					objects_to_delete.append(obj)

			print(f"Number of objects to delete in file {fileName}: {len(objects_to_delete)}")

			# If there are matching objects, ask the user whether to continue
			if len(objects_to_delete) > 0:
				# confirm whether user would like to continue
				if force in {'y', 'Y'}:
					choice = 'y'
				else:
					choice = input("Do you want to continue? (y/n): ")
			
				if choice in {'y', 'Y'}:
					count = 0

					# Remove the matching objects from the object
					for obj in objects_to_delete:
						data.remove(obj)
						count += 1

					print(f"\nNumber of objects deleted: {count}\n")

					# Write the updated object back to the current JSON file
					with open(fileName, 'w', encoding='utf-8') as f:
						json.dump(data, f)
						print(f"Updated file: {fileName}\n")

				if choice in {'n', 'N'}:
					print("Skipping the file...\n")

				if choice not in {'y', 'Y', 'n', 'N'}:
					print("\nInvalid choice. Exiting the program...\n")
					break

			# If there are no matching objects, skip the file
			else:
				print("No objects to delete in file {fileName}. Skipping file...\n")
	else:
		print("\nNo objects to delete in any file. Exiting the program...")
else:
	print(f"\nNo endsong files found in directory '{directory}'. Exiting the program...")
