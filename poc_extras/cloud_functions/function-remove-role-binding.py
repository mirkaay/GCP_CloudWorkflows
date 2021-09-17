import argparse
import os

from google.oauth2 import service_account
import googleapiclient.discovery

def main(request):
    """Gets IAM policy for a project."""
    service = googleapiclient.discovery.build("cloudresourcemanager", "v1")
    print('REQUEST IS {}'.format(request))
    request_json = request.get_json(silent=True)
    print('REQUEST_JSON IS {}'.format(request_json))
    print('SERVICE IS {}'.format(service))
    policy = (
        service.projects()
        .getIamPolicy(
            resource=request_json['project'],
            body={"options": {"requestedPolicyVersion": 1}},
        )
        .execute()
    )
    print('CURRENT IAM policy is {}'.format(policy))
    # return policy

#  Remove member from a role binding

    get_current_iam_bindings_for_role = [ b for b in policy["bindings"] if b["role"] == request_json['role'] ]
    binding = {"role": request_json['role'], "members": request_json['member']}
    print('BINDING is {}'.format(binding))
    print('IAM POLICY BEFORE REMOVING BINDING IS {}'.format(policy))
    # search your current IAM policy bindings json (policy["bindings"])
    print('BEFORE        GET_CURRENT_IAM_BINDINGS_FOR_ROLE IS {}'.format(get_current_iam_bindings_for_role[0]['members']))
    get_current_iam_bindings_for_role[0]['members'].remove(request_json['member'])
    print('AFTER        GET_CURRENT_IAM_BINDINGS_FOR_ROLE IS {}'.format(get_current_iam_bindings_for_role[0]['members']))
    # policy["bindings"].remove(binding)
    print('IAM POLICY AFTER REMOVING BINDING IS {}'.format(policy))

    policy = (
        service.projects()
        .setIamPolicy(resource=request_json['project'], body={"policy": policy})
        .execute()
    )
    print('POLICY IS {}'.format(policy))
    return policy

# [END iam_modify_policy_add_member]

