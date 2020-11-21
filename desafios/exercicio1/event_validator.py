import json
import boto3

with open(schema_path, 'r') as j:
    schema = json.load(j)
class EventValidator:
    def __init__(self, schema_path, _SQS_CLIENT) -> None:
        with open(schema_path, 'r') as j:
            self.schema = json.load(j)

        self._SQS_CLIENT = _SQS_CLIENT

    def get_schema(self) -> dict:
        return self.schema

    def __get_required(self) -> list:
        return set(self.schema['required'])

    def __checkrequired(self, event:dict) -> (bool, str):
        check = self.__get_required().symmetric_difference(list(event.keys()))

        if len(check) == 0:
            return (True, "All required fields are filled")
        else:
            missed = self.__get_required() - set(list(event.keys()))
            if len(missed) == len(self.__get_required):
                return (False, "Invalid fields: " + str(set(list(event.keys()))\
                                                    - self.__get_required()))
            else:
                return (False, "Missed fields: " + str(missed))

    set(schema['required']).symmetric_difference(list(event.keys()))


    def send_event_to_queue(self, event:dict, queue_name:str) -> None:
        '''
        Responsável pelo envio do evento para uma fila
        :param event: Evento  (dict)
        :param queue_name: Nome da fila (str)
        :return: None
        '''

        sqs_client = boto3.client("sqs", region_name="us-east-1")
        response = sqs_client.get_queue_url(
            QueueName=queue_name
        )
        queue_url = response['QueueUrl']
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(event)
        )
        print(f"Response status code: [{response['ResponseMetadata']['HTTPStatusCode']}]")


    def handler(self, event):
        '''
        #  Função principal que é sensibilizada para cada evento
        Aqui você deve começar a implementar o seu código
        Você pode criar funções/classes à vontade
        Utilize a função send_event_to_queue para envio do evento para a fila,
            não é necessário alterá-la
        '''
        print("Entrei no handler")
        print("Event: ", event)


