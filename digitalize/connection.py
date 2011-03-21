#!/usr/bin/python

from kombu.connection import BrokerConnection
from kombu.messaging import Consumer, Exchange, Producer, Queue
from logger import logger

def create_connection(config):
    conn = BrokerConnection(config.get("connection", "hostname"),
                                  config.get("connection", "userid"),
                                  config.get("connection", "password"),
                                  config.get("connection", "virtual_host"))
    channel = conn.channel()

    return channel

def produce_msg_document(channel, document, queue_name):
    private_exchange = Exchange(queue_name, "direct", durable=True)
    producer = Producer(channel, exchange=private_exchange, serializer="pickle")
    producer.publish(document, routing_key=queue_name)
    logger.debug("message produced")

def produce_msg_image(channel, image_name, image, queue_name):
    private_exchange = Exchange(queue_name, "direct", durable=True)
    producer = Producer(channel, exchange=private_exchange, serializer="pickle")
    producer.publish(document, routing_key=queue_name)
    logger.debug("message produced")

def process_document(document, message):
    print document
    message.ack()

def consume_msg(channel):
    private_exchange = Exchange("private", "direct", durable=True)
    document_queue = Queue("private", exchange=private_exchange,
                           routing_key="private")
    consumer = Consumer(channel, document_queue, callbacks=[process_document])
    #consumer.register_callback(process_document)
    consumer.consume()
    while True:
        channel.connection.drain_events()

