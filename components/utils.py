import json

class Utils(object):
    @classmethod
    def extract_json_objects(cls, data):
        """Extract JSON objects from a concatenated string."""
        objects = []  # List to store extracted JSON objects
        pos = 0  # Position in the string
        
        # Loop through the string to extract JSON objects
        while pos < len(data):
            # Decode a JSON object from the string starting at position 'pos'
            obj, pos = json.JSONDecoder().raw_decode(data, pos)
            objects.append(obj)
            
            # Skip any whitespace or extra characters between objects (no need as we strip white space in main)
            # while pos < len(data) and data[pos].isspace():
            #     pos += 1
        
        return objects  # Return the list of extracted JSON objects
