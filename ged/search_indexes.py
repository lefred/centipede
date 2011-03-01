from haystack.indexes import CharField, RealTimeSearchIndex
from haystack import site
from ged.models import Document, Page


class PageIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    file_name = CharField(model_attr='file_name')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Page.objects.all()

class DocumentIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    document_name = CharField(model_attr='name')
    genre = CharField(model_attr='genre')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Document.objects.all()

site.register(Page, PageIndex)
site.register(Document, DocumentIndex)
