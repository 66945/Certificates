import re
import zipfile
from zipfile import ZipFile

"""
The Document class is used to interact with Microsoft Word (TM) documents on
a Windows machine.

This class uses an attribute replacement system, similar to madlibs.

In order for the document to be edited it must have the desired attributes
surrounded by brackets. These can later be replaced.

Ex:

My dog has [attrib]

in order to change that, you would use Document.replaceAttrib('attrib', 'fleas')

When you call Document.close() the final file will output to the specified outpath
"""
class Document:
    path = ''
    outpath = ''
    docpath = ''

    content = ''

    def __init__(self, path, outpath):
        self.path = path
        self.outpath = outpath

        with ZipFile(self.path, 'r') as zip:
            self.docpath = 'word/document.xml'

            with ZipFile(self.outpath, 'w') as outZip:
                paths = zip.namelist()

                for path in paths:
                    if path != self.docpath:
                        content = zip.read(path)
                        outZip.writestr(path, content, compress_type=zipfile.ZIP_DEFLATED)

            self.content = zip.read(self.docpath).decode('UTF-8')
    
    # Behavior specified above
    def replaceAttrib(self, attrib, replacement):
        attrib = '[' + attrib + ']'

        self.content = self.content.replace(attrib, replacement, 1)

    # Behavior specified above
    def close(self):
        with ZipFile(self.outpath, 'a') as zip:
            zip.writestr(self.docpath, self.content.encode('UTF-8'), compress_type=zipfile.ZIP_DEFLATED)

def main():
    doc = Document('test.docx', 'test_out.docx')
    doc.replaceAttrib('name', 'Mr. Monkeyface')
    doc.close()

if __name__ == '__main__':
    main()