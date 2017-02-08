import datetime
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from marketing.forms import PromotionForm
from django.core.mail import EmailMessage


class PromoQuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock("quote title")
    attribution = blocks.CharBlock()

    class Meta:
        icon = "openquote"


class ImageFormatChoiceBlock(blocks.FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class PromoStreamBlock(blocks.StreamBlock):
    h2 = blocks.CharBlock(icon="title", classname="title")
    h4 = blocks.CharBlock(icon="title", classname="title")
    aligned_image = ImageBlock(label="Picture", icon="image")
    intro = blocks.RichTextBlock(icon="pilcrow")
    paragraph = blocks.RichTextBlock(icon="pilcrow")
    promoquote = PromoQuoteBlock(label="Quote")


class Category(Page):
    parent_page_types = ['marketing.Category']
    subpage_types = ['marketing.Category', 'marketing.Promotion']

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Promotion(Page):
    PRIORITIES = [
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
    ]
    EMAIL_STATUS = [
        ('0', 'Queued'),
        ('1', 'Sended'),
    ]

    parent_page_types = ['marketing.Category']
    subpage_types = []

    subject = models.CharField(verbose_name=_('Subject'), max_length=100)
    priority = models.CharField(verbose_name=_('Priority'), default='0', max_length=1, null=True, blank=True,
                                choices=PRIORITIES)
    email_status = models.CharField(verbose_name=_('Email Status'), default='', max_length=1, null=True, blank=True,
                                    choices=EMAIL_STATUS)
    # content = RichTextField()
    content = StreamField(PromoStreamBlock())
    email_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Emails file list'),
        help_text='Only excel are allowed! xls and xlsx file extensions.'
    )
    email_by_user = models.PositiveIntegerField(
                        verbose_name=_('Qty emails'),
                        help_text='Choose how many emails per client you want to send during the promotion.', default=1,
                        validators=[MaxValueValidator(5), MinValueValidator(1)]
                    )

    created_at = models.DateTimeField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel('email_status', classname="fields priority-field"),
        FieldPanel('subject', classname="fields subject-field"),
        FieldPanel('email_by_user', classname="fields qty-email-field"),
        FieldPanel('priority', classname="fields priority-field"),
        StreamFieldPanel('content'),
        DocumentChooserPanel('email_document'),
    ]

    base_form_class = PromotionForm

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
