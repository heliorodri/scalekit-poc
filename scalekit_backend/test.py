import os

from flask import jsonify
from scalekit_backend.client.scalekit_client import ScClient
from scalekit.v1.clients.clients_pb2 import OrganizationClient

sc = ScClient()

org_id = str(os.environ.get('SCALEKIT_ORG_ID'))

# List connections by organization id
connections = sc.connection.list_connections(
  organization_id=org_id
)

# List connections by domain
response = sc.connection.list_connections_by_domain(domain="google.com")
print(response[0])