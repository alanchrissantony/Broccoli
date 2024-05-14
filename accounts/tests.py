from django.test import TestCase
from json import JSONEncoder
import datetime
# Create your tests here.
    
class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return super().default(obj)
