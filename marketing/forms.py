from wagtail.wagtailadmin.forms import WagtailAdminPageForm
import pprint
from django import forms
from django.utils.translation import ugettext_lazy as _
import xlrd
import os.path

# from django.utils.translation import ugettext_lazy as _
# from wagtail.wagtailadmin.edit_handlers import FieldPanel
# from wagtail.wagtailcore.models import Page

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

class PromotionForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        page = super(PromotionForm, self).save(commit=False)
        pp = pprint.PrettyPrinter(depth=6)
        if page.email_document:
            media_dir = os.path.join(BASE_DIR, 'promotion/media/documents/')
            pp.pprint(media_dir)
            pp.pprint(page.email_document.filename)
            pp.pprint("File path!")

            workbook = xlrd.open_workbook(os.path.join(media_dir, page.email_document.filename))
            workbook.sheet_names()
            sheet_line = workbook.sheet_by_index(0)


        if commit:
            page.save()
        return page

    def clean(self):
        cleaned_data = super(PromotionForm, self).clean()
        email_document = cleaned_data.get("email_document")
        pp = pprint.PrettyPrinter(depth=6)

        if email_document.file_extension not in ['xlsx', 'xls']:
            pp.pprint(email_document.file_extension)
            pp.pprint("Invalid file extension!")
            raise forms.ValidationError(
                _('Invalid file extension: %s'),
                code='invalid',
                params={'value': email_document.file_extension},
            )
