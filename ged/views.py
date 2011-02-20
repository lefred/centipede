from centipede.ged.models import Page, Document
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader, Context
from kombu.connection import BrokerConnection
from kombu.messaging import Consumer, Exchange, Queue

def create_connection():
    conn = BrokerConnection("localhost",
                            "fred",
                            "fred123",
                            "arsia")
    channel = conn.channel()

    return channel

def process_document(document, message):
    user = User.objects.get(username="fred")
    s_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    doc = Document(name = document.name, genre = document.genre, scanning_date = s_date, user = user)
    doc.save()
    print "document %s saved" % doc.name
    i = 0
    for sfile in document.files:
        page = Page(file_name = sfile, ocr = document.ocr[i], barcodes = document.barcodes[i], document = doc)
        i += 1
        page.save()
        print "    page %s saved" % sfile
    message.ack()

def consume_msg(channel):
    compta_exchange = Exchange("compta", "direct", durable=True)
    document_queue = Queue("compta", exchange=compta_exchange,
                           routing_key="compta")
    consumer = Consumer(channel, document_queue, callbacks=[process_document])
    #consumer.register_callback(process_document)
    consumer.consume()
    while True:
        channel.connection.drain_events()


def consume_document(request):
    channel = create_connection()
    consume_msg(channel)

def show_document(request, document_id=''):
    document = Document.objects.get(id=document_id)
    pages = Page.objects.filter(document=document_id)

    t = loader.get_template('Document.html')
    c = Context({"document": document,
                 "pages": pages})
    return HttpResponse(t.render(c))


