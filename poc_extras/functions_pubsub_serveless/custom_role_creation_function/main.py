import argparse
import os

from google.oauth2 import service_account
import googleapiclient.discovery

service = googleapiclient.discovery.build('iam', 'v1')

def create_role(name, project, title, description, permissions, stage, member):
    """Creates a role."""

    # pylint: disable=no-member
    role = service.projects().roles().create(
        parent='projects/' + project,
        body={
            'roleId': name,
            'role': {
                'title': title,
                'description': description,
                'includedPermissions': permissions,
                'stage': stage
            }
        }).execute()

    print('Created role: ' + role['name'])
    return role

    binding = next(b for b in policy["bindings"] if b["role"] == role)
    binding["members"].append(member)
    print(binding)
    return policy

# [END iam_create_role]

def main(data, context):
    project = "<PROJECT ID>"
    name = 'boppermisbah'
    title = 'misbah-test-role'
    description = 'misbah-test-role'
    permissions = 'compute.disks.create'
    stage = 'GA'
    member = '<EMAIL ID>'

    create_role(name, project, title, description, permissions, stage, member)

