import argparse
import os

from google.oauth2 import service_account
import googleapiclient.discovery

def main(request):
    """Gets IAM policy for a project."""
    service = googleapiclient.discovery.build("cloudresourcemanager", "v1")
    request_json = request.get_json(silent=True)
    print('service is {}'.format(service))
    policy = (
        service.projects()
        .getIamPolicy(
            resource=request_json['project'],
            body={"options": {"requestedPolicyVersion": 1}},
        )
        .execute()
    )
    print('policy is {}'.format(policy))
    # return policy

# [START iam_modify_policy_add_member]
#  Adds a new member to a role binding

    print('policy["bindings"] is {}'.format(policy["bindings"]))
    give_it_a_name = [ b for b in policy["bindings"] if b["role"] == request_json['role'] ]
    print('give_it_a_name is {}'.format(give_it_a_name))
    binding = {"role": request_json['role'], "members": request_json['member']}
    print('binding is {}'.format(binding))
    policy["bindings"].append(binding)
    policy = (
        service.projects()
        .setIamPolicy(resource=request_json['project'], body={"policy": policy})
        .execute()
    )
    # print(binding)
    return policy

# [END iam_modify_policy_add_member]

