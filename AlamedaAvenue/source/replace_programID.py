# Define the file path
file_path = 'spain.add.xml'

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Replace all instances of programID="0" with programID="tls"
modified_content = content.replace('programID="0"', 'programID="tls"')

# Write the modified content back to the file
with open(file_path, 'w') as file:
    file.write(modified_content)

print("Replacement complete.")
