#! /usr/bin/python
"""
The original Publisher Subscriber Design pattern would be implemented over the network with the publisher and subscribers \
being remotely located and both using a common messaging messaging queue/broker to communicate/interact, without ever \
knowing about each other directly. This gives rise to a loosely coulpled architecture for message passing.

However, this is an example implementation which is all local in a client machine and doesnt involve network programming.\
The publishers, subscribers and message broker are all classes in the same machine, but this is not how they would be in real setting.\
Where they would be 3 different components in preferably 3 different servers/clients for reliability.

So assume that all the 3 components/classes present here are running on 3 different servers/clients and interact over the \
network by knowing each other's internet addresses.

However, since this is not a network-based implementation, and no addresses are involved. Assume that publishers and \
subscribers know about the broker using a broker instance available with them, instead of an IP address here.
Similarly, the broker has an instance of subscribers with itself to send appropriate messages to subscribers instead of their\
IP addresses.
"""

import logging
from collections import defaultdict

class Broker:
    """Message Broker / Middle-ware that hosts the message queue and is responsible for making communication possible \
    between publishers and subscribers, without them knowing about each other"""

    def __init__(self):
        """Initialize the Message Queue broker with an empty resource set - message queue and subscriber/topic mapping.
           This will happen only once in time (hopefully) when the message queue is first started and should run continually"""
        self.messaging_queue = []
        self.topic_subscription_mapping = defaultdict(lambda:[])

    def run_loop(self):
        """This is the main code in the broker which always runs until message queue has more messages to pass\
        else, it waits for any more messages. """
        for message in self.messaging_queue:
            message, topic = self.process_message(message)
            subscribers = self.get_subscribers_for_topic(topic)
            self.push_message_to_subscribers(subscribers, message)

    def on_message(self, message):
        if len(message.split(";")) >= 2:
            self.messaging_queue.append(message)
            logger.info("Message received by queue :  " + message)
        else:
            pass

    def process_message(self, message):
        message_parts = message.split(";")
        return message_parts[0], message_parts[1]

    def get_subscribers_for_topic(self, topic):
        subscribers = self.topic_subscription_mapping[topic]
        return subscribers

    def push_message_to_subscribers(self, subscribers, message):
        for subscriber in subscribers:
            subscriber.on_message(message)

    def subscribe_to_topic(self, subscriber, topic):
        self.topic_subscription_mapping[topic].append(subscriber)

    def topic_data(self, subscriber, topic):
        messages_for_topic = [self.process_message(message)[0] for message in self.messaging_queue if self.process_message(message)[1] == topic]
        message_aggregator = ""
        for message in messages_for_topic:
            message_aggregator += message + "..."
        self.push_message_to_subscribers([subscriber], message_aggregator)


class Publisher:
    """Publisher that publishes topic wise content into the message broker"""

    def __init__(self, name, broker):
        self.name = name
        self._Broker = broker

    def publish(self, message, topic):
        _message = message + ";" + topic
        logger.info(self.name + "  , Publishing a message : " + message + " in topic :  " + topic)
        self._Broker.on_message(_message)


class Subscriber:
    """Subscriber that subscribes to topics with the broker"""

    def __init__(self, name, broker):
        self.name = name
        self._Broker = broker

    def subscribe(self, topic):
        self._Broker.subscribe_to_topic(self, topic)

    def get_topic_data(self, topic):
        self._Broker.topic_data(self, topic)

    def on_message(self, message):
        logger.info(self.name + "  , Received a message : " + message)


def main():
    logger.info("Starting Message Broker Service")

    broker = Broker()

    s1 = Subscriber("subscriber 1", broker)
    s2 = Subscriber("subscriber 2", broker)
    s3 = Subscriber("subscriber 3", broker)
    p1 = Publisher("publisher 1", broker)
    p2 = Publisher("publisher 2", broker)

    s1.subscribe("Sports")
    s1.subscribe("Politics")
    s2.subscribe("Sports")
    s2.subscribe("Politics")
    s3.subscribe("Politics")

    p1.publish("Message 1", "Politics")
    p1.publish("Message 2", "Sports")
    p1.publish("Message 4", "Politics")
    p1.publish("Message 5", "Politics")
    p1.publish("Message 7", "Politics")

    broker.run_loop()

    s3.get_topic_data("Politics")

    logger.info("Ending Message Broker Service")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler('pub_sub.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    main()
