from .utils import Utils
import sys

class Scanner(object):
    @classmethod
    def scan(cls):
        commands = []        
        while True:
            try:
                # Continuously read input from stdin
                stuff = input().strip()
                if not stuff:  # If empty input (e.g., enter is pressed without input), continue
                    continue
                new_commands = Utils.extract_json_objects(stuff)
                commands.extend(new_commands)
            except EOFError:  # End of input (Ctrl+D on Unix or Ctrl+Z on Windows)
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                continue  # Continue reading inputs despite errors
        return commands