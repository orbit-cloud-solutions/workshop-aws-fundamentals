import aws_cdk as core
import aws_cdk.assertions as assertions

from workshop_8.workshop_8_stack import Workshop8Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in workshop_8/workshop_8_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Workshop8Stack(app, "workshop-8")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
