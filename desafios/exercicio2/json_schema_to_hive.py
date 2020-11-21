import json
import logging

log = logging.getLogger('schema_to_hive')

class Athena:
    '''
    Athena class to execute queries
    '''
    def __init__(self, schema_path: str, ATHENA_CLIENT: 'client.Athena'):
        '''
        Initialize Athena class
        '''
        self._ATHENA_CLIENT = ATHENA_CLIENT
        with open(schema_path, 'r') as j:
            self.schema = json.load(j)
        self.__init_types()

    def __get_properties(self) -> dict:
        '''
        Get properties
        '''
        return self.schema['properties']

    def __get_schema(self) -> dict:
        '''
        Get schema
        '''
        return self.schema

    def __init_types(self) -> None:
        '''
        Define types to use in the query
        '''
        self.types = {'string': 'STRING', 'integer': 'INT',
                        'object': 'STRING', 'boolean': 'BOOLEAN'}


    def __create_hive_table_with_athena(self, query: str) -> None:
        '''
        Create hive table with athena
        '''
        log.info(f"Query: {query}")
        try:
            self._ATHENA_CLIENT.start_query_execution(
                QueryString=query,
                ResultConfiguration={
                    'OutputLocation': f's3://iti-query-results/'
                }
            )
            log.info("Query executed successfully")
        except Exception as e:
                msg = 'Failed to execute query: ' + str(e)
                log.error(msg)

    def __build_query(self) -> str:
        '''
        Build the query to create the hive table
        '''
        schema = self.__get_schema()
        properties = self.__get_properties()

        table_name = "_".join(schema['title'].split(' '))
        query = "CREATE EXTERNAL TABLE IF NOT EXISTS " + table_name + " ( "

        for field in list(properties.keys()):
            query +=  field + " " + self.types[properties[field]['type']] + ", "
        query += ")"
        return query

    def handler(self):
        '''
        Handle query creation
        '''
        query = self.__build_query()
        self.__create_hive_table_with_athena(query)