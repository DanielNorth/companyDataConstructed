from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader
import os


def _getFields(obj, tree=None, retval=None, fileobj=None):
    """
    Extracts field data if this PDF contains interactive form fields.
    The *tree* and *retval* parameters are for recursive use.

    :param fileobj: A file object (usually a text file) to write
        a report to on all interactive form fields found.
    :return: A dictionary where each key is a field name, and each
        value is a :class:`Field<PyPDF2.generic.Field>` object. By
        default, the mapping name is used for keys.
    :rtype: dict, or ``None`` if form data could not be located.
    """
    fieldAttributes = {'/FT': 'Field Type', '/Parent': 'Parent', '/T': 'Field Name', '/TU': 'Alternate Field Name',
                       '/TM': 'Mapping Name', '/Ff': 'Field Flags', '/V': 'Value', '/DV': 'Default Value'}
    if retval is None:
        retval = OrderedDict()
        catalog = obj.trailer["/Root"]
        # get the AcroForm tree
        if "/AcroForm" in catalog:
            tree = catalog["/AcroForm"]
        else:
            return None
    if tree is None:
        return retval

    obj._checkKids(tree, retval, fileobj)
    for attr in fieldAttributes:
        if attr in tree:
            #print(attr)
            # Tree is a field
            obj._buildField(tree, retval, fileobj, fieldAttributes)
            break

    if "/Fields" in tree:
        fields = tree["/Fields"]
        for f in fields:
            field = f.getObject()
            obj._buildField(field, retval, fileobj, fieldAttributes)
            print(f)

    return retval


def get_form_fields(infile):
    infile = PdfFileReader(open(infile, 'rb'))
    fields = _getFields(infile)
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())


def changeNAR1Form(outfile_loc, companynumber, companyName, businessname, newvals=None):
    infile = os.getcwd() + '\\companyFilling\\static\\pdfFile\\NAR1_fillable.pdf'
    outfile = os.getcwd() + f'\\companyFilling\\static\\pdfFile\\nar1_company_form\\{outfile_loc}.pdf'
    print('fuck')
    print(outfile)

    # infile = '\\companyFilling\\static\\pdfFile\\NAR1_fillable.pdf'
    # outfile = f'\\companyFilling\\static\\pdfFile\\nar1_company_form\\{outfile}.pdf'

    pdf = PdfFileReader(open(infile, 'rb'))
    writer = PdfFileWriter()

    fillingOrder = [companynumber, companyName, businessname]
    for _ in range(100):
        fillingOrder.append('nothing')

    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        try:
            if newvals:
                writer.updatePageFormFieldValues(page, newvals)
            else:
                writer.updatePageFormFieldValues(page, {k: f'{fillingOrder[i]}-{i} {k}' for i, (k, v) in
                                                        enumerate(get_form_fields(infile).items())
                                                        })
            writer.addPage(page)
        except Exception as e:
            print(repr(e))
            writer.addPage(page)

    with open(outfile, 'wb') as out:
        writer.write(out)

    return str(outfile)



