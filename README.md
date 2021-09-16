The break glass process involved following steps to achieve the stated goal:

Developer breaks glass by creating a pull request on GitHub and then getting it merged to main/master branch.

This will then trigger a GH Action to provision a VM on GCP.

A custom role will be created for the developer with appropriate permissions.

Add that custom role to an IAM policy binding including the developer’s user email.

Remove the IAM policy binding, delete the custom role, and delete VM after a pre-defined timeframe.

 There were several concerns with the sequence of this workflow in terms of passing variables from GitHub actions and selection of suitable GCP resources for a serverless approach. The initial design involved multiple GCP resources; Cloud Functions for provisioning and deleting each resource, Pub/Sub to pass parameters and trigger functions, and a Cloud Scheduler.

The solution fulfilled the objectives but raised concerns over multiple services in action, where breaking of one service during the break glass process will result in failure. A different approach was utilized using Cloud Workflows while achieving the same results.         

# Cloud Workflows

Cloud Workflows was used instead to create serverless workflow that linked series of steps together in an order defined. Users can manage workflows from the Google Cloud Console, from the command line using the Cloud SDK, or using the REST API. Key features of Cloud Workflows include:

- Reliable Workflow execution

- Built-in error handling

- Passing variable values between steps

- Cloud Logging

Cloud Workflows defines a series of step definitions in a sequential manner, but with integrating the jump instructions and conditions, it is easy to get lost between the order of steps. Fortunately, the ability to visualize the Cloud Workflow definition while editing in real time has been introduced in GCP. Currently, Cloud Workflows is only available in us-central1, asia-southeast1, and Europe-west4.

# Solution

 The solution was created by utilizing Cloud Workflows and Cloud Build containers. Provisioning of resources such as VM and IAM roles was handled by calling API’s defined in Workflow steps. Cloud Build containers were used to add and remove IAM policy bindings using a gcloud command instead of using a Cloud Function or by calling an API. 
 
![workflows diagram (1)](https://user-images.githubusercontent.com/53059374/133540672-6f94117f-8239-4b9b-ad5c-c71ee525fd7e.jpg)

