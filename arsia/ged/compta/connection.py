#!/usr/bin/python

from kombu.connection import BrokerConnection
from kombu.messaging import Consumer, Exchange, Producer, Queue


def create_connection(config):
    conn = BrokerConnection(config.get("connection", "hostname"),
                                  config.get("connection", "userid"),
                                  config.get("connection", "password"),
                                  config.get("connection", "virtual_host"))
    channel = conn.channel()

    return channel

def produce_msg(channel, document):
    compta_exchange = Exchange("compta", "direct", durable=True)
    producer = Producer(channel, exchange=compta_exchange, serializer="pickle")
    producer.publish(document, routing_key="compta")

def process_document(document, message):
    print document.ocr

def consume_msg(channel):
    compta_exchange = Exchange("compta", "direct", durable=True)
    document_queue = Queue("compta", exchange=compta_exchange,
                           routing_key="compta")
    consumer = Consumer(channel, document_queue, callbacks=[process_document])
    consumer.register_callback(process_document)
    #consumer.register_callback(process_document)
    consumer.consume()
    while True:
        channel.connection.drain_events()

