import PyPDF2
from PIL import Image
from PIL.ExifTags import TAGS
from optparse import OptionParser

# 提取PDF的元数据
def getPDF(fileName):
    pdfFile = PyPDF2.PdfFileReader(open(fileName,'rb'))
    pdfInfo = pdfFile.getDocumentInfo()
    print("\n[*] PDF MetaData for %s\n"%fileName)
    for iterm in pdfInfo:
        print('[+]',iterm,':',pdfInfo[iterm])

# 提取图片的元数据
def getpic(fileName):
    image = Image.open(fileName)
    info = image._getexif()
    print("\n[*] Picture MetaData for %s\n"%fileName)
    if info:
        for (tag,valu) in info.items():
            text = TAGS.get(tag)
            print('[+]',text,':',valu)
    

if __name__ == "__main__":
    # 命令行参数
    parse = OptionParser()
    parse.add_option('-f','--file',dest='file',help='The file to extract metadata.(.pdf .jpg .png)')
    (options , args) = parse.parse_args()
    end = ['pdf','jpg','png']
    if options.file:
        if options.file.split('.')[-1] not in end:
            print('[-] Invalid suffix!')
            exit()
        if options.file.split('.')[-1] == 'pdf':
            getPDF(options.file)
        else:
            getpic(options.file)
    else:
        parse.print_help()
        print('\nExample:')
        print('[#]-> python MetaData.py -f test.pdf')
        print('[#]-> python MetaData.py -f test.jpg')
