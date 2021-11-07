import re
from database import get_collection
class Query(object):
    '''
    classdocs
    '''


    def __init__(self):
        print("query start")
        
    def parse_user_input(self, input_string):
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
        field_value_pattern = re.compile(r'\:((\s[>,<]{1}\s[0-9]+)|(\"[a-zA-Z0-9]+\")|([a-zA-Z0-9]+)|(\sNOT\s[a-zA-Z0-9]+)|([a-zA-Z0-9]+\sAND\s[a-zA-Z0-9]+)|([a-zA-Z0-9]+\sOR\s[a-zA-Z0-9]+))$')
        content = re.search(field_value_pattern, input_string)
        
        if content is None:
            raise ValueError('content invalid format, [<,>] operators should be used with numbers, AND, NOT, OR needs keywords')
        else:
            content = content.group(0)
    
        return obj, field, content
    
    def valid_parse(self, obj, field):
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
        self.valid_parse(obj, field)
        obj = obj.replace('.',"")
        obj = obj.strip()
        
        field = field.replace('.',"")
        field = field.replace(':',"")
        field = field.strip()
        content = content.replace(":","")
        print(obj, field, content)
        if "<" in content:
            return self.handle_less(obj, field, content)
        elif ">" in content:
            return self.handle_greater(obj, field, content)
        elif '"' in content:
            return self.handle_quotes(obj, field, content)
        elif "AND" in content:
            return self.handle_and(obj, field, content)
        elif "OR" in content:
            return self.handle_or(obj, field, content)
        elif "NOT" in content:
            return self.handle_not(obj, field, content)
        else:
            return self.handle_standard(obj, field, content)
        
    def is_num(self, input_string):
        for c in input_string:
            if c.isdigit():
                input_string = int(input_string)
                return input_string
        return input_string
        
    def clean_content(self, content, tmp):
        cont = content.replace(tmp,"")
        cont = cont.strip()
        return cont
    
    def handle_greater(self, obj, field, content):
        tmp = ">"
        cont = self.clean_content(content,tmp)
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find():
            if int(i[field]) > int(cont):
                collection_list.append(i)
                
        return collection_list
    
    def handle_less(self, obj, field, content):
        tmp = "<"
        cont = self.clean_content(content,tmp)
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find():
            if int(i[field]) < int(cont):
                collection_list.append(i)
                
        return collection_list
    
    def handle_quotes(self, obj, field, content):
        tmp = '"'
        cont = self.clean_content(content,tmp)
        print(cont)
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find():
            if i[field] == cont:
                collection_list.append(i)
            
        return collection_list 
    
    #USE SPLIT
    def handle_and(self, obj, field, content):
        cont = content.split(" ")
        condition_1 = cont[0]
        condition_2 = cont[2]
        
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find():
            if condition_1 in i[field] and condition_2 in i[field]:
                collection_list.append(i)
        
        return collection_list 
    
    def handle_or(self, obj, field, content):
        cont = content.split(" ")
        condition_1 = cont[0]
        condition_2 = cont[2]
        
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find():
            if condition_1 in i[field] or condition_2 in i[field]:
                collection_list.append(i)
        
        return collection_list 
    
    def handle_not(self, obj, field, content):
        cont = content.strip()
        cont = cont.split(" ")
        cont = cont[1]
        
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find():
            if cont not in i[field]:
                collection_list.append(i)
                
        return collection_list
    
    def handle_standard(self,obj, field, content):
        cont = content
        collection_list = []
        collection = self.get_collection(obj)
        
        for i in collection.find():
            if cont in i[field]:
                collection_list.append(i)
            
        return collection_list
    
    def get_collection(self, obj):
        return get_collection()
    
if __name__ == '__main__':
    D = Query()
    obj, f, c = D.parse_user_input('champion.name:Akal')
    print(obj, f, c)
    print(D.query_handler(obj, f, c))