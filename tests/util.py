from django.conf import settings

from django.db.models import (
    Model,
    CharField
)

from cassandra.cqlengine.connection import get_cluster
from cassandra.cqlengine.management import delete_keyspace

from djangocassandra.db.backends.cassandra.base import DatabaseWrapper
from djangocassandra.db.backends.cassandra.compiler import SQLInsertCompiler


def connect_db():
    connection = DatabaseWrapper(settings.DATABASES['default'])
    connection_params = connection.get_connection_params()
    connection.get_new_connection(connection_params)
    return connection


def create_model(connection, model):
    connection.creation.sql_create_model(
        model,
        None
    )


def populate_db(connection, values):
    for value in values:
        value.save()    


def destroy_db(connection):
    if None is not connection:
        keyspace_names = [
            key for key in settings.DATABASES['default']['KEYSPACES'].keys()
        ]
        for keyspace in keyspace_names:
            delete_keyspace(keyspace)
