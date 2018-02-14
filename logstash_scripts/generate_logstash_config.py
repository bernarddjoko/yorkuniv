import csv
from logstash_config_template import LogstashTemplate




class LogstashConfigGenerator: 

    

    def generateMutateClause(self, column,coltype):
        template = """mutate {{convert => ["{column}", "{coltype}"]}}"""
        dct = {"column":column, "coltype":coltype}
        mutate_clause = template.format(**dct)
        return mutate_clause    



    def generateMutateClauses(self,headers_specs_path):
        mutate_list = []
        with open(headers_specs_path, "r") as csvfile:
            headers_reader = csv.reader(csvfile, delimiter=',')
            for row in headers_reader:
                column_name = (row[0].strip()).lower()
                column_type =  (row[1].strip()).lower()
                mutate_list.append(self.generateMutateClause(column_name, column_type))
                
        mutate_clauses = "\n".join(mutate_list)  
        return mutate_clauses

    def getColumn_list(self,headers_specs_path): 
        column_list = []
        with open(headers_specs_path, "r") as csvfile:
            headers_reader = csv.reader(csvfile, delimiter=',')
            for row in headers_reader:
                column_name = (row[0].strip()).lower()
                column_list.append(column_name)
                
        return column_list

    
    def generateConfig(self,index_name, document_type, separator, 
        data_path, headers_specs_path):
        logstash_template = LogstashTemplate()
        mutate_clauses = self.generateMutateClauses(headers_specs_path)
        column_list = self.getColumn_list(headers_specs_path)
        values_dict = {"path":data_path, 
                        "separator": separator,
                        "columns_list":  column_list,
                        "mutate_list":mutate_clauses,
                        "index":index_name, 
                        "document_type":document_type
                        } 
        logstash_config = logstash_template.fillTemplate(values_dict) 
        return logstash_config               
                     
def main(args):
    index_name = args[0]
    document_type = args[1]
    separator = args[2]
    data_path = args[3]
    headers_specs_path = args[4]
    l = LogstashConfigGenerator()
    
    config = l.generateConfig(index_name, document_type, separator, 
        data_path, headers_specs_path)
    return config  

        

        



if __name__ == "__main__": 
    import sys
    args = sys.argv[1:]
    print(main(args))

    
