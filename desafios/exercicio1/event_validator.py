import json
import boto3
import logging

log = logging.getLogger('event_validator')

class EventValidator:
    '''
    Class to validate events
    '''
    def __init__(self, schema_path: str, queue_name: str) -> None:
        '''
        Initialize EventValidator class
        '''
        self.__init_types()
        with open(schema_path, 'r') as j:
            self.schema = json.load(j)

        self.queue_name = queue_name

    def __init_types(self) -> None:
        '''
        Define types to validate
        '''
        self.types = {'string': str, 'integer': int,
                        'object': dict, 'boolean': bool}

    def __get_required(self) -> set:
        '''
        Get required fields
        '''
        return set(self.schema['required'])

    def __get_properties(self) -> dict:
        '''
        Get properties
        '''
        return self.schema['properties']

    def __checkrequired(self, event:dict) -> bool:
        '''
        Check if all required fields are available
        '''
        check = self.__get_required().symmetric_difference(list(event.keys()))

        if len(check) == 0:
            log.info("All required fields are available")
            return True
        else:
            missed = self.__get_required() - set(list(event.keys()))
            log.error("Missed fields: " + str(missed))
            return False

    def __checkinvalid(self, event:dict) -> bool:
        '''
        Check  fields not registered in the schema
        '''
        invalid = set(list(event.keys())) - self.__get_required()
        if len(invalid) > 0:
            log.error("Unrecognized field(s): " + str(invalid))
            return False
        else:
            log.info("All fields are valid")
            return True

    def __checktypes(self, event:dict) -> bool:
        '''
        Check fields with unexpected types
        '''
        properties = self.__get_properties()
        invalid = False
        for field in list(properties.keys()):
            if type(event[field]) != self.types[properties[field]['type']]:
                msg = field + " invalid type. Expected " + \
                      properties[field]['type'] + " but got " + \
                      str(type(event[field]))
                log.error(msg)
                invalid = True
        if invalid:
            return False
        else:
            log.info("All types are valid")
            return True

    def send_event_to_queue(self, event:dict) -> None:
        '''
        Send events to the queue
        '''
        sqs_client = boto3.client("sqs", region_name="us-east-1")
        response = sqs_client.get_queue_url(
            QueueName=self.queue_name
        )
        queue_url = response['QueueUrl']
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(event)
        )
        log.info(f"Response status code: \
            [{response['ResponseMetadata']['HTTPStatusCode']}]")

    def handler(self, event: dict) -> None:
        '''
        Handle new events
        '''
        if self.__checkrequired(event) and self.__checkinvalid(event) and \
            self.__checktypes(event):
            try:
                self.send_event_to_queue(event)

            except Exception as e:
                msg = 'Failed to insert event into the queue: ' + str(e)
        else:
            log.error("Failed to insert event into the queue")
