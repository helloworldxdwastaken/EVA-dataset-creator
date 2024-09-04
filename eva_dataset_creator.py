import os
import json
from termcolor import colored

def print_ascii_art(text):
    print(colored(text, "magenta", attrs=["bold"]))

def print_with_color(text, color="magenta"):
    print(colored(text, color))

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_blocks(content, file_name):
    try:
        data = json.loads(content)
        messages = []
        for item in data.get("messages", []):
            if "role" in item and "content" in item:
                messages.append(item)
        return {"messages": messages}
    except ValueError as e:
        print_with_color(f"Ignoring file '{file_name}' due to invalid JSON. Error: {str(e)}", "yellow")
        return None

def merge_files_in_folder(folder_path, allowed_extensions):
    folder_name = os.path.basename(folder_path)
    merged_content = {"messages": []}

    for file in os.listdir(folder_path):
        if os.path.splitext(file)[1].lower() in allowed_extensions:
            file_path = os.path.join(folder_path, file)
            content = read_file(file_path)
            block = extract_blocks(content, file)

            if block:
                merged_content["messages"].extend(block["messages"])

    output_file_path = f"{os.path.splitext(folder_path)[0]}_merged.json"
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(merged_content, out_file, ensure_ascii=False, indent=4)

    print_with_color(f"\nMerged '{colored(folder_name, 'cyan')}'s files into '{colored(output_file_path, 'green')}'\n")

def main():
    print_ascii_art(r"""
          _____                    _____                    _____          
         /\    \                  /\    \                  /\    \         
        /::\    \                /::\____\                /::\    \        
       /::::\    \              /:::/    /               /::::\    \       
      /::::::\    \            /:::/    /               /::::::\    \      
     /:::/\:::\    \          /:::/    /               /:::/\:::\    \     
    /:::/__\:::\    \        /:::/____/               /:::/__\:::\    \    
   /::::\   \:::\    \       |::|    |               /::::\   \:::\    \   
  /::::::\   \:::\    \      |::|    |     _____    /::::::\   \:::\    \  
 /:::/\:::\   \:::\    \     |::|    |    /\    \  /:::/\:::\   \:::\    \ 
/:::/__\:::\   \:::\____\    |::|    |   /::\____\/:::/  \:::\   \:::\____\
\:::\   \:::\   \::/    /    |::|    |  /:::/    /\::/    \:::\  /:::/    /
 \:::\   \:::\   \/____/     |::|    | /:::/    /  \/____/ \:::\/:::/    / 
  \:::\   \:::\    \         |::|____|/:::/    /            \::::::/    /  
   \:::\   \:::\____\        |:::::::::::/    /              \::::/    /   
    \:::\   \::/    /        \::::::::::/____/               /:::/    /    
     \:::\   \/____/          ~~~~~~~~~~                    /:::/    /     
      \:::\    \                                           /:::/    /      
       \:::\____\                                         /:::/    /       
        \::/    /                                         \::/    /        
         \/____/                                           \/____/         

""")
    print_with_color("Enhanced Virtual Assistant (E.V.A.) - DB Creator\n")

    input("Press enter to start...")

    database_folder = "database"

    if not os.path.exists(database_folder):
        print_with_color("The specified 'database' directory does not exist.", "red")
        return

    allowed_extensions = ['.json', '.md', '.txt', '.csv']

    for folder in os.listdir(database_folder):
        if os.path.isdir(os.path.join(database_folder, folder)):
            merge_files_in_folder(os.path.join(database_folder, folder), allowed_extensions)

if __name__ == "__main__":
    main()
