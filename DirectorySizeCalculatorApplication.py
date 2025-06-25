import os
from typing import Dict, List, Union

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def __str__(self):
        return f"{self.name} ({self.size} bytes)"

class Directory:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.contents: Dict[str, Union[File, Directory]] = {}

    def add_file(self, name: str, size: int):
        self.contents[name] = File(name, size)

    def add_directory(self, name: str):
        self.contents[name] = Directory(name, self)

    def get_size(self) -> int:
        total_size = 0
        for item in self.contents.values():
            if isinstance(item, File):
                total_size += item.size
            elif isinstance(item, Directory):
                total_size += item.get_size()
        return total_size

    def __str__(self):
        return f"{self.name}/"

class FileSystem:
    def __init__(self):
        self.root = Directory("root")
        self.current_dir = self.root

    def cd(self, path: str):
        if path == "/":
            self.current_dir = self.root
            return
        
        if path == "..":
            if self.current_dir.parent is not None:
                self.current_dir = self.current_dir.parent
            return

        # Handle relative paths
        target_dir = self.current_dir
        parts = path.split("/")
        
        for part in parts:
            if not part:
                continue  # skip empty parts from leading/trailing/multiple slashes
                
            if part == "..":
                if target_dir.parent is not None:
                    target_dir = target_dir.parent
                continue
            
            if part in target_dir.contents and isinstance(target_dir.contents[part], Directory):
                target_dir = target_dir.contents[part]
            else:
                print(f"Directory not found: {part}")
                return

        self.current_dir = target_dir

    def ls(self):
        print(f"Contents of {self.current_dir.name}:")
        for name, item in self.current_dir.contents.items():
            print(f"  - {item}")

    def size(self):
        total_size = self.current_dir.get_size()
        print(f"Total size of {self.current_dir.name}: {total_size} bytes")

    def mkdir(self, dir_name: str):
        if dir_name in self.current_dir.contents:
            print(f"Directory '{dir_name}' already exists")
        else:
            self.current_dir.add_directory(dir_name)

    def touch(self, file_name: str, size: int):
        if file_name in self.current_dir.contents:
            print(f"File '{file_name}' already exists")
        else:
            self.current_dir.add_file(file_name, size)

def main():
    fs = FileSystem()
    
    # Create some sample data
    fs.mkdir("documents")
    fs.cd("documents")
    fs.touch("report.txt", 1500)
    fs.touch("notes.txt", 800)
    fs.mkdir("projects")
    fs.cd("projects")
    fs.touch("project1.py", 3000)
    fs.touch("project2.py", 2500)
    fs.cd("..")
    fs.cd("..")
    fs.mkdir("pictures")
    fs.cd("pictures")
    fs.touch("vacation.jpg", 4500)
    fs.mkdir("screenshots")
    fs.cd("screenshots")
    fs.touch("screen1.png", 1200)
    fs.touch("screen2.png", 1800)
    fs.cd("/")
    
    print("Welcome to the Directory Size Calculator!")
    print("Available commands: cd, ls, size, mkdir, touch, exit")
    
    while True:
        try:
            command = input(f"{fs.current_dir.name}> ").strip().split()
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == "cd":
                if len(command) > 1:
                    fs.cd(command[1])
                else:
                    print("Usage: cd <directory>")
                    
            elif cmd == "ls":
                fs.ls()
                
            elif cmd == "size":
                fs.size()
                
            elif cmd == "mkdir":
                if len(command) > 1:
                    fs.mkdir(command[1])
                else:
                    print("Usage: mkdir <directory_name>")
                    
            elif cmd == "touch":
                if len(command) > 2:
                    try:
                        size = int(command[2])
                        fs.touch(command[1], size)
                    except ValueError:
                        print("Size must be an integer")
                else:
                    print("Usage: touch <file_name> <size>")
                    
            elif cmd == "exit":
                break
                
            else:
                print("Unknown command. Available commands: cd, ls, size, mkdir, touch, exit")
                
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()