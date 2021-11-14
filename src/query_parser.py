import re
from database import get_collection
class Query(object):
    '''
    QUERY class handles our query parsing for our application and is heavily based on the
    query parser produced in assignment 2
    '''
    def __init__(self):
        print("query start")
        
    def parse_user_input(self, input_string):
        """
        Function to check if the user input is a valid query and breaks query into
        object, field and content
        """
        form = re.compile(r"^[a-zA-Z]+\.[a-zA-Z\_]+\:.*$")
        f = re.search(form, input_string)
        if f is None:
            raise ValueError('bad format, q not in form of obj.field:content')
        
        
        obj_pattern = re.compile(r"^[a-zA-Z]+\.")
        obj = re.search(obj_pattern, input_string)
        
        if obj is None:
            raise ValueError('Object:bad format')
        else:
            obj = obj.group(0)
            
        field_pattern = re.compile(r"\.[a-zA-Z\_]+\:")
        field = re.findall(field_pattern, input_string)
        
        if field is None:
            raise ValueError('field, invalid format')
        elif len(field) > 1:
            raise ValueError('too many operators')
        else:
            field = field[0]
        field_value_pattern = re.compile(r'\:((\s[>,<]{1}\s[0-9]+)|([a-zA-Z0-9]+\s{0,1}[a-zA-Z0-9]*))$')
        content = re.search(field_value_pattern, input_string)
        
        if content is None:
            raise ValueError('content invalid format, [<,>] operators should be used with numbers, AND, NOT, OR needs keywords')
        else:
            content = content.group(0)
    
        return obj, field, content
    
    def valid_parse(self, obj, field):
        """
        Checks the values of the parsed object, field, and content
        """
        obj_tmp = obj.replace('.',"")
        obj_tmp = obj_tmp.strip()
        
        if obj_tmp != "champion":
            raise ValueError('Object, bad value')
        
        
        
        field_tmp = field.replace('.',"")
        field_tmp = field_tmp.replace(':',"")
        field_tmp = field_tmp.strip()
        
        model_dict = {"name": "Lex",
                "win_rate" : "79%",
                "pick_rate" : "48%",
                "champ_tier" : "Tier 4",
                "counter_champs" : ["Azir","Yasuo", "Yone"],
                "strong_against" : ["Zed", "Akali", "Alistar"],
                }
        
        if obj_tmp == "champion" and field_tmp not in model_dict.keys():
            raise ValueError('Field, bad value for author')
        
        return None
    
    def query_handler(self, obj, field, content):
        """
        cleans the object, field, content and
        then calls the right function to properly handle the query
        """
        self.valid_parse(obj, field)
        obj = obj.replace('.',"")
        obj = obj.strip()
        
        field = field.replace('.',"")
        field = field.replace(':',"")
        field = field.strip()
        content = content.replace(":","")
        print(obj, field, content)
        print(content)
        if "<" in content:
            return self.handle_less(obj, field, content)
        elif ">" in content:
            return self.handle_greater(obj, field, content)
        else:
            return self.handle_standard(obj, field, content)
        
    def clean_content(self, content, tmp):
        """
        cleans the content for the functions
        """
        cont = content.replace(tmp,"")
        cont = cont.strip()
        return cont
    
    def handle_greater(self, obj, field, content):
        """
        handles the greater than function
        """
        tmp = ">"
        cont = self.clean_content(content,tmp)
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find({},{'_id':0}):
            if float(i[field].strip('%')) > float(cont):
                collection_list.append(i)
                
        return collection_list
    
    def handle_less(self, obj, field, content):
        """
        handles the less than function
        """
        tmp = "<"
        cont = self.clean_content(content,tmp)
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find({},{'_id':0}):
            if float(i[field].strip('%')) < float(cont):
                collection_list.append(i)
                
        return collection_list
    
    
    def handle_standard(self,obj, field, content):
        """
        handles the normal operation without any symbols
        """
        cont = content
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find({},{"_id":0}):
            if cont in i[field]:
                collection_list.append(i)
            
        return collection_list
    
    def get_collection(self, obj):
        """
        gets the right collection
        """
        return get_collection()
    
if __name__ == '__main__':
    D = Query()
    obj, f, c = D.parse_user_input('champion.win_rate: > 55')
    print(obj, f, c)
    print(D.query_handler(obj, f, c))