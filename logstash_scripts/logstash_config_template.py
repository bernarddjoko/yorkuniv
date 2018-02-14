

class LogstashTemplate:


    def __init__(self):
    
         self.values_dict = {"path":"/Users/yardman/development/york_university/yorkuniv/data/cameoeventcodes/*.csv", 
                        "separator": ",",
                        "columns_list": ["CAMEOEVENTCODE","EVENTDESCRIPTION"],
                        "mutate_list":"""mutate {convert => ["CAMEOEVENTCODE", "integer"]}""",
                        "index":"gdelt", 
                        "document_type":"cameoevents"
                        } 

    def fillTemplate(self, values_dict):

        self.template = """
            input {{
                file {{
                    path => "{path}"
                    start_position => "beginning"
                    sincedb_path => "/dev/null"
                    }}

                }}

            filter{{
                    csv {{
                            separator => "{separator}"
                            columns => {columns_list}

                        }}
                    {mutate_list}
                    

            }}

                output {{

                        elasticsearch {{
                        hosts => "localhost:9200"
                        index => "{index}"
                        document_type => "{document_type}"
                        }}

                    stdout{{}}

                    }}
        """

        val = self.template.format(**values_dict)
        return val




