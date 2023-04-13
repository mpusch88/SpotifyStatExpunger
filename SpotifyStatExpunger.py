import json
import os
import re

# get the current working directory from the user
directory = input("\nEnter the directory path:  ")

# find number of files matching the pattern endsong_*.json in directory
num_files = len([f for f in os.listdir(directory) if re.match(r'endsong_.*\.json', f)])

if num_files > 0:
		print(f"\n  Number of endsong files in directory '{directory}': {num_files}")

quit = False
while not quit:
	if num_files > 0:
		# get the string to search for from the user
		pattern = input("\nEnter the string to search for:  ")

		#convert the string to regular expression
		pattern = pattern.replace(" ", "\s")
		pattern = r'\{.*' + pattern + r'.*\}'

		print("\n Searching for the following regular expression:  " + pattern + "\n")

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
			force = input("\nDo you want to force all updates? (y/n):  ")
			print()

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

				# If there are matching objects, ask the user whether to continue
				if len(objects_to_delete) > 0:
					choice = -1

					# confirm whether user would like to continue
					if force in {'y', 'Y'}:
						choice = 'y'
					else:
						print(f"{fileName} - {len(objects_to_delete)} objects to delete.\n")
						choice = input("Delete: 'A'll, 'I'ndividual, 'S'kip, 'Q'uit:  ")

					if choice in {'q', 'Q'}:
						print("\nExiting the program...\n")
						break

					if choice not in {'y', 'Y', 'n', 'N', 'a', 'A', 'i', 'I', 's', 'S'}:
						print("\nInvalid choice. Exiting the program...\n")
						break
					
					if choice in {'n', 'N', 's', 'S'}:
						print(f"{fileName} / Skipping the file...\n")

					if choice in {'y', 'Y', 'a', 'A'}:
						count = 0

						# Remove the matching objects from the object
						for obj in objects_to_delete:
							data.remove(obj)
							count += 1

						# Write the updated object back to the current JSON file
						with open(fileName, 'w', encoding='utf-8') as f:
							json.dump(data, f)
							if force in {'y', 'Y'}:
								print(f"{fileName} - {count} objects out of {len(objects_to_delete)} deleted.")
							else:
								print(f"\n{fileName} - {count} objects deleted. Continuing to next file...\n")

					if choice in {'i', 'I'}:
						count = 0

						# Remove the matching objects from the object
						for obj in objects_to_delete:
							current = json.dumps(obj, indent=4, sort_keys=True)

							if not force in {'y', 'Y'}:
								podcast = True
								# print the object to be deleted
								for line in current.splitlines():
									if '"episode_name": null,' in line:
										podcast = False

									if podcast:
										if "episode_name" in line:
											print("\n" + "  Episode:	" + line.split(":")[1].strip('", ').replace('"', ''))
										if "episode_show_name" in line:
											print("  Show:		" + line.split(":")[1].strip('", ').replace('"', '') + "\n")
									else:
										if "master_metadata_album_album_name" in line:
											print("\n" + "  Album:	" + line.split(":")[1].strip('", ').replace('"', ''))
										if "master_metadata_album_artist_name" in line:
											print("  Artist:	" + line.split(":")[1].strip('", ').replace('"', ''))
										if "master_metadata_track_name" in line:
											print("  Track:	" + line.split(":")[1].strip('", ').replace('"', '') + "\n")

								choice = input("Delete this object? ('Y'es, 'N'o, 'A'll, 'S'top):  ")

								if choice in {'s', 'S'}:
									break

								if choice in {'y', 'Y'}:
									data.remove(obj)
									print("Object deleted.\n")
									count += 1

								if choice in {'a', 'A'}:
									data.remove(obj)
									print("Deleting all remaining objects...\n")
									count += 1
									force = 'y'

								if choice not in {'y', 'Y', 'a', 'A'}:
									print("Object not deleted.\n")

							else:
								data.remove(obj)
								count += 1

						# Write the updated object back to the current JSON file
						with open(fileName, 'w', encoding='utf-8') as f:
							json.dump(data, f)
							print(f"{fileName} - {count} objects deleted. Continuing to next file...\n")
							force = 'n'

				# If there are no matching objects, skip the file
				else:
					print(f"{fileName} - No objects to delete. Skipping file...")

			# if force not in {'y', 'Y', 'a', 'A'}:
			searchAgain = input("\nPress enter to search again... ('Q' to quit)  ")

			if searchAgain not in {'q', 'Q'}:
				continue
			else:
				print("\nExiting the program...\n")
				quit = True
				break

		else:
			searchAgain = input("\nNo objects to delete in any file. Press enter to search again... ('Q' to quit)  ")
			if searchAgain not in {'q', 'Q'}:
				continue
			else:
				print("\nExiting the program...")
				break

	else:
		print(f"\nNo endsong files found in directory '{directory}'. Exiting the program...")
		break
