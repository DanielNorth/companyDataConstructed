from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader

companyNumber = 'Company Number to be filled'
companyName = 'Company Name to be filled'
businessName = 'business name to be filled'


fillingOrder = [companyNumber, companyNumber, businessName]
for i in range(1000):
    fillingOrder.append(i)


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


def update_form_values(infile, outfile, newvals=None):
    pdf = PdfFileReader(open(infile, 'rb'))
    writer = PdfFileWriter()

    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        try:
            if newvals:
                writer.updatePageFormFieldValues(page, newvals)
            else:
                writer.updatePageFormFieldValues(page, {k: f'{fillingOrder[i]}---{i} {k}={v}' for i, (k, v) in
                                                        enumerate(get_form_fields(infile).items())
                                                        })
            writer.addPage(page)
        except Exception as e:
            print(repr(e))
            writer.addPage(page)

    with open(outfile, 'wb') as out:
        writer.write(out)


if __name__ == '__main__':
    from pprint import pprint

    pdf_file_name = 'NAR1_fillable.pdf'

    pprint(get_form_fields(pdf_file_name))

    update_form_values(pdf_file_name, 'out-' + pdf_file_name)  # enumerate & fill the fields with their own names
    update_form_values(pdf_file_name, 'out2-' + pdf_file_name,
                       {'my_fieldname_1': 'My Value',
                        'my_fieldname_2': 'My Another Value'})  # update the form fields