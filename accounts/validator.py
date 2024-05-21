import re

class Validator:
    @staticmethod
    def validate_name(value):
        # Define the regular expression pattern for valid names
        pattern = re.compile(r'^[a-zA-Z\s]+$')
        return not bool(pattern.match(value))
    
    @staticmethod
    def validate_email(value):
        # Define the regular expression pattern for a valid email address
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return not bool(pattern.match(value))
    
    @staticmethod
    def validate_password(value):
        # Define the regex pattern for the password
        pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        return not bool(pattern.match(value))
    
    @staticmethod
    def validate_discount(value):
        return value > 100 or value < 0
    
    @staticmethod
    def validate_data(value):
        pattern = re.compile(r'^[a-zA-Z0-9\s]+$')
        return not bool(pattern.match(value))