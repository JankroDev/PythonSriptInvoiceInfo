import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class InvoiceReader:
    def readInvoice(self):
        # Get the list of all files and directories
        path = r'C:\\Users\\dellclient\\Desktop\\EliteInvoices\\'
        dir_list = os.listdir(path)

        for invoice in dir_list:
            print(invoice)
            img = cv2.imread(path + invoice)

            invoiceNumber = getInvoiceNumber(img, path+ invoice).strip()
            date = getDate(img).strip()
            totalText = getTotal(img).strip()

            newfilename = invoiceNumber + "_" + date + "_" + totalText
            absolutepath = os.path.abspath(path) +"\\"+ newfilename

            os.rename(path+invoice, absolutepath+".jpg")


def getParts(img):
    partNumbersList = getPartNumbers(img)
    print("RawParts Text: " + partNumbersList)
    return "UnderConstruction"

def getInvoiceNumber(img, path):
    y = 2663
    x = 1900
    h = 359
    w = 136
    crop = img[y:y + h, x:x + w]
    invoicetext = pytesseract.image_to_string(crop)
    invoicenumber = invoicetext.strip()
    print("First Invoice number Grab: " + invoicenumber)
    if len(invoicenumber) == 6:
        return invoicenumber
    else:
        print("Trying Invoice Number Again")
        y = 2650
        x = 1850
        h = 400
        w = 200
        crop = img[y:y + h, x:x + w]
        invoicetext = pytesseract.image_to_string(crop)
        invoicenumber = invoicetext.strip()
        splitInvoiceNumber = invoicenumber.split()
        if len(splitInvoiceNumber) > 1:
            print("Invoice Number Grabbed after retry: " + splitInvoiceNumber[0])
            return splitInvoiceNumber[0]

        print("Invoice Number Grabbed after retry: " + invoicenumber)

        return invoicenumber

def getDate(img):
    y = 2325
    x = 606
    h = 1070
    w = 500
    crop = img[y:y + h, x:x + w]
    text = pytesseract.image_to_string(crop)
    date = text.find("Date:")
    dateText = text[date + 6: date + 16]
    dateText = dateText.replace('/', "")
    dateText = dateText.strip()
    return dateText

def getTotal(img):
    y = 1913
    x = 530
    h = 320
    w = 150
    crop = img[y:y + h, x:x + w]
    totaltext = pytesseract.image_to_string(crop)
    substring = '.'
    if substring in totaltext:
        print("Found the Dot")
        return totaltext.strip()

    else:
        print("Resizing the Total once")
        resized = resizeForCorrection(crop)
        totaltext = pytesseract.image_to_string(resized)
        if '.' in totaltext:
            return pytesseract.image_to_string(resized).strip()
        else:
            print("Trying to resize total one more time")
            y = 1850
            x = 450
            h = 400
            w = 200
            crop = img[y:y + h, x:x + w]
            totaltext = pytesseract.image_to_string(crop)
            splitstring = totaltext.split()
            if len(splitstring) > 1:
                print("Grabbed two totals")
                totaltext = splitstring[0]
            return  totaltext.strip()

def resizeForCorrection(img):
    scale_percent = 110  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    print("Couldn't find dot, resizing")
    return resized

def showImage(crop):
    cv2.imshow("Invoice Image", crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def getPartNumbers(img):
    y = 55
    x = 877
    h = 600
    w = 2300
    crop = img[y:y + h, x:x + w]
    text = pytesseract.image_to_string(crop)
    showImage(crop)

    print("RawPartNumbers Text: " + text)
    return text



ir = InvoiceReader()
ir.readInvoice()

