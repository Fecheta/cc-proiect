from azure.cosmos import exceptions, CosmosClient, PartitionKey


class DBConnection(object):

    def __init__(self, type):
        self.endpoint = "https://cloudproiect.documents.azure.com:443/"
        self.key = 'uKKz1Ik9lEBtWOMqvSnbwxXfEDQOj5zJjQA4Ynl6w1hiV8jjx7Hzn613lKQsNhL8GlEBVaqLUHKhUqOYVLa3BQ=='
        self.client = CosmosClient(self.endpoint, self.key)
        if type== "Users":
            self.database_name = 'Users'
        else:
            self.database_name = 'Documents'
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        if type == "Users":
            self.container_name = 'Users'
        else:
            self.container_name = 'Documents'
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )

    def insert_user(self,id, email, username, password):
        self.container.upsert_item({
            'id': '{0}'.format(id),
            'email': '{0}'.format(email),
            'password': '{0}'.format(password),
            'username': '{0}'.format(username)
        }
        )

    def insert_document(self, id, user_id, image_url, pdf_url, language):
        self.container.upsert_item({
            'id': '{0}'.format(id),
            'user_id': '{0}'.format(user_id),
            'image_url': '{0}'.format(image_url),
            'pdf_rl': '{0}'.format(pdf_url),
            'language': '{0}'.format(language)
        }
        )
    def select_user(self, id):
        query = "SELECT * FROM c WHERE c.id='{0}'".format(id)

        items = list(self.container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        print(items)
        return items

    def select_document(self, id):
        query = "SELECT * FROM c WHERE c.id='{0}'".format(id)

        items = list(self.container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        print(items)
        return items

    def get_RU(self):
        request_charge = self.container.client_connection.last_response_headers['x-ms-request-charge']
        print('Operation consumed {0} request units'.format(request_charge))
