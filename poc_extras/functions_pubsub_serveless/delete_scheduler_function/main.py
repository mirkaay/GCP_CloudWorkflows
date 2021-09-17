from googleapiclient import discovery

# [START DELETE SCHEDULER]
def delete_scheduler(data, context):
    print("About to delete Scheduler1")
    service = discovery.build('cloudscheduler', 'v1')
    print("About to delete Scheduler2")
    print('printing requestor {}'.format(data['attributes']['virtualmachine']))
    default = str(data['attributes']['virtualmachine'])
    name = "projects/<PROJECT ID>/locations/us-central1/jobs/{}".format(default)
    #print(name)
    #print(name.__class__)
    # name = "projects/<PROJECT ID>/locations/us-central1/jobs/mir-misbahuddin"
    print("About to delete Scheduler3")
    request = service.projects().locations().jobs().delete(name=name)
    request.execute()
    print("deleted?")
    #print("About to delete Scheduler5")
    #delete_scheduler(data=5, context="deleted")
    #print("Scheduler Deleted!!")
# [END DELETE SCHEDULER]

