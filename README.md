# Publisher-Subscriber-Implementation
This is a simple implementation of Publisher/Subscriber implementation in Python on a single machine and not over the network.

The original Publisher Subscriber Design pattern would be implemented over the network with the publisher and subscribers
being remotely located and both using a common messaging messaging queue/broker to communicate/interact, without ever
knowing about each other directly. This gives rise to a loosely-coupled architecture for message passing.

However, this is an example implementation which is all local in a client machine and doesnt involve network programming.
The publishers, subscribers and message broker are all classes in the same machine, but this is not how they would be in real setting. Where they would be 3 different components in preferably 3 different servers/clients for reliability. Say, all the 3 components/classes present here are running on 3 different servers/clients and interact over the
network by knowing each other's internet addresses.

However, since this is not a network-based implementation, and no addresses are involved. Assume that publishers and
subscribers know about the broker using a broker instance available with them, instead of an IP address here.
Similarly, the broker has an instance of subscribers with itself to send appropriate messages to subscribers instead of their
IP addresses.

# Design Philosophy

Broker is a component / class which has the resources for message queue and subscriber-topic mapping.
It also has methods to add subscriber to a topic subscription list, cleaning messages, accepting messages from publishers, for aggregation of messages upon request of subscribers and to finally send the appropriate messages to subscribers who subscribed to that given topic.

Publisher component / class has a Broker instance that it uses to pass along messages to the broker along with methods to publish these messages to the queue.

Subscriber component / class again has a broker instance that it uses to register itself with topics and request aggregation of messages for a given topic. Also it has a callback method used as an event on receipt of a new message from the broker.

These are 3 loosely connected components, publishers and subscribers are aware of only the message queue in between and are unaware of each other's existence.
