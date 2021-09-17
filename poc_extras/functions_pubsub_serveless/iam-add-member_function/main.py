import argparse
import os

from google.oauth2 import service_account
import googleapiclient.discovery

def get_policy(project_id, role, member, title, expression, description, version= (3)):
    """Gets IAM policy for a project."""
    service = googleapiclient.discovery.build("cloudresourcemanager", "v1")
    print('service is {}'.format(service))
    policy = (
        service.projects()
        .getIamPolicy(
            resource=project_id,
            body={"options": {"requestedPolicyVersion": version}},
        )
        .execute()
    )
    print('policy is {}'.format(policy))
    # return policy

# [START iam_modify_policy_add_member]
#  Adds a new member to a role binding

    print('policy["bindings"] is {}'.format(policy["bindings"]))
    give_it_a_name = [ b for b in policy["bindings"] if b["role"] == role ]
    print('give_it_a_name is {}'.format(give_it_a_name))
    binding = {"role": role, "members": [member], "condition": {"title": title, "description": description, "expression": expression}}
    print('binding is {}'.format(binding))
    policy["bindings"].append(binding)
    policy = (
        service.projects()
        .setIamPolicy(resource=project_id, body={"policy": policy})
        .execute()
    )
    # print(binding)
    return policy

# [END iam_modify_policy_add_member]

def main(data, context):
    print('data is {}'.format(data))
    print('context is {}'.format(context))
    project_id = 'golang-misbah03'
    role = 'projects/golang-misbah03/roles/boppiemisbah'
    member = 'serviceAccount:misbah-sa-02@golang-misbah03.iam.gserviceaccount.com'
    title = 'expirable access'
    description = 'expirable access'
    expression = 'request.time < timestamp("2021-07-15T12:05:00.000Z")'
    get_policy(project_id, role, member, title, expression, description, version= (3))

