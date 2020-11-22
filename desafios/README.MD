
## Challenge solution

### Exercício 1

O primeiro exercicio foi resolvido seguindo as instruções fornecidas. Realizei pequenas alterações na assinatura das funções para colocar todos os métodos dentro de uma única classe (`EventValidator`). Além disso, adicionei um aquivo de configuração de logs para padronizar as mensagens.

O código pode ser testado a partir do seguinte comando:

    python exercicio1/main.py


Para verificar o funcionamento dos métodos, recomendo alterar os campos do dicionário `event` presente em `main.py`


### Exercício 2

O segundo exercicio foi resolvido seguindo as instruções fornecidas. Realizei pequenas alterações na assinatura das funções para colocar todos os métodos dentro de uma única classe (`Athena`). Além disso, adicionei um aquivo de configuração de logs para padronizar as mensagens.

O código pode ser testado a partir do seguinte comando:

    python exercicio1/main.py



### Exercício 3

Para a construção da arquitetura, tentei ser o menos dependente de uma cloud específica. Optei por descrever o que será utilizado e os serviços disponíveis na AWS, GCP ou ferramentas open-source. A ideia é focar nas funcionalidades, não nas ferramentas.

Para lidar com os eventos, optei por utilizar Pub/Sub por se tratar de um serviço de mensagens em tempo real. Visando escalabilidade e facilidade de manutenção, podem ser utilizados serviços totalmente gerenciados como o Pub/Sub do GCP ou Amazon SNS. Caso o objetivo seja não ficar dependente de nenhuma cloud, Apache Kafka ou Pulsar podem ser utilizados.



Escolhi esse modelo de ingestão de dados pensando na necessidade de escalabilidade dos eventos, a ideia
é que os eventos sejam divididos por tipos - cada tipo de evento terá um canal de comunicação exclusivo.

Os serviços de Pub/Sub possuem buffer próprio para armazenar os eventos em uma fila, essa fila será consumida por métodos que verificam a qualidade
dos dados. Irei assumir que cada tipo de evento possui um esquema único e, portanto, necessita de métodos próprios para que a qualidade do
dados seja verificada.

Assim como feito no exercício 1, esses métodos serão criados com base nos esquemas associados a cada tipo de evento. Tais esquemas estarão
armazenados em um `document-oriented databased` e servirão como base para a construção dos nós de `Data Cleansing` e `Data Transformation`. 
O nó de data cleansing será responsável por consumir os dados a partir dos tópicos pub/sub associados a cada tipo de evento e corrigir ou remover dados corrompidos ou incorretos.

Já a etapa de data transformation, consite em converter os dados de um formato para outro, visando armazenar as informações de maneira consistente em um Data Warehouse.

Esses nós podem construídos de forma customizada em python (como feito nos exercícios), ou serem construídos com base em ferramentas de criação de fluxo de ETL como o Apache Beam, ou utilizando aplicações de clouds como o GCP DataFlow ou AWS Glue.


Uma vez que os dados tenham sido processados, eles serão amarmazenados em um Data warehouse. Aqui, a ideia é usar coisas como GCP BigQuery, AWS Redshift ou Apache Hive. Todas as opções são focadas em escala e processamento de grandes volumes de dados.


O objetivo é que toda a arquitetura seja monitorada por uma stack `ELK (ElasticSearch, Logstash e Kibana)` com informações acerca de desempenho de cada uma das máquinas e containers e também logs de execução dos códigos e possíveis errors. O kibana fornece uma interface com dashboards que faclitam todo esse monitoramento.


Por fim, o usuário poderá acessar todos os dados de eventos armazenados no Data warehouse para a realização de análises exploratórias dos dados e modelagem.

![](./images/architecture-iti.png =750x)





