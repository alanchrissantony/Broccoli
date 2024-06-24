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
    
    @staticmethod
    def validate_stock(value):
        try:
            value = int(value)
            return value < 0
        except:
            return False
    
    @staticmethod
    def validate_price(price):
        try:
            float_price = float(price)
            return float_price <= 0  # Stock price should not be negative
        except ValueError:
            return False