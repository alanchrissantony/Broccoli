import re

class Validator:
    def validate_name(value):
    # Define the regular expression pattern for valid names
        pattern = r'^[a-zA-Z\s]+$'
        # Check if the value matches the pattern
        if not re.match(pattern, value):
            return True
        return False
    

    def validate_email(value):
        # Define the regular expression pattern for a valid email address
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Check if the value matches the pattern
        if not re.match(pattern, value):
            return True
        return False
    
    def validate_password(value):
    # Define the regex pattern for the password
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, value):
            return True
        return False
    
    def validate_discount(value):
        if value > 100 or value < 0:
            return True
        return 
    
    def validate_data(value):
        pattern = r'^[a-zA-Z0-9\s]+$'
        if not re.match(pattern, value):
            return True
        return False