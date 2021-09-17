import argparse
import os

from google.oauth2 import service_account
import googleapiclient.discovery

def get_policy(project_id, role, member):
    """Gets IAM policy for a project."""
    service = googleapiclient.discovery.build("cloudresourcemanager", "v1")
    print('GCP_PROJECT is {}'.format(os.environ.get('GCP_PROJECT', 'Specified environment variable is not set.')))
    print('service is {}'.format(service))
    policy = (
        service.projects()
        .getIamPolicy(
            resource=project_id,
            body={},
        )
        .execute()
    )
    print('policy is {}'.format(policy))
    # return policy

# [START iam_modify_policy_add_member]
#  Adds a new member to a role binding

    print('policy["bindings"] is {}'.format(policy["bindings"]))
    # print('policy["bindings"]["role"] is {}'.format(policy["bindings"]["role"]))
    give_it_a_name = [ b for b in policy["bindings"] if b["role"] == role ]
    print('give_it_a_name is {}'.format(give_it_a_name))
    # next(b for b in policy["bindings"] if b["role"] == role)
    # binding = next(b for b in policy["bindings"] if b["role"] == role)
    binding = {"role": role, "members": [member]}
    # binding["members"].append(member)
    print('binding is {}'.format(binding))
    policy["bindings"].append(binding)
    print('policy is NOW AFTER ALL THIS WORK {}'.format(policy))
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
    # print('data[attributes][project_id] is {}'.format(data['attributes']['project_id']))
    project_id = str(data['attributes']['project_id'])
    role = str(data['attributes']['role'])
    member = str(data['attributes']['member'])

# print('project_id is {}, role is {}, member is {}'.format(data['attributes']['project_id'], data['attributes']['role'], data['attributes']['member']))

    get_policy(project_id, role, member)

