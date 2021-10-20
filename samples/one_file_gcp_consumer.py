import asyncio
from pydrinker.managers import DrinkerManager
from pydrinker_gcp.routes import SubscriptionRoute

#
# Configurations to change about your GCP configuration
#

GCP_PROJECT_ID = "xablau-123"  # change the value to your project id on google cloud provider
GCP_SUBSCRIPTION_ID = "sample-subscription"  # change the value to your subscription id on
                                             # google cloud provider


#
# Options to tunning GCP pull client over pydrinker
#

provider_options = {
    "options": {
        "deadline": 300.0,    # How long to keep retrying in seconds
        "max_messages": 100,  # The maximum number of messages to return for 1 pull request
        "timeout": None,      # The timeout for 1 pull request
    }
}

#
# Handler to process the message
#


async def print_handler(message, *args):
    print("Let's consume a message!")
    print(f"message, {message}")
    print(f"args, {args}")

    # fake IO processing
    await asyncio.sleep(0.1)

    # this True send a ACK to provider and
    # delete the message from subscriber
    return True

#
# Configuration to map subscriptions to handlers through the routes
#

routes = (
    SubscriptionRoute(
        project_id=GCP_PROJECT_ID,
        subscription_id=GCP_SUBSCRIPTION_ID,
        provider_options=provider_options,
        handler=print_handler,
    ),
)

#
# The manager to manage process of your consumer
#

manager = DrinkerManager(routes=routes)
manager.run()
