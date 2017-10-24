# -*- coding: utf-8 -*-

"""
ITrak
Command line invoice tracking

Authors:
    Tristan Henning <tristan@customcrypto.com>
    
    If you want to contribute, please feel free to do so.

This software uses the BSD Licence. You can find a copy at the bottom of the
source code. 
"""

TAX_RATE = 0.0775

class Payment(object):
    def __init__(self, paymentType, paymentTotal, whoPayed, paymentDate, paymentID=None):
        self.how = paymentType
        self.who = whoPayed
        self.total = paymentTotal
        self.ID = paymentID
        self.date = paymentDate
    def whoPaid(self):
        return self.who
    def howMuch(self):
        return self.total
    def method(self):
        return self.how
    def getID(self):
        return self.ID
    def getDate(self):
        return self.date


class Client(object):
    def __init__(self, clientName):
        self.name = clientName
        self.address = None
        self.city = None
        self.contact = None
        self.type = None
        self.phone1 = None
        self.phone2 = None
        self.fax = None
        self.email = None

class Invoice(object):
    """
    Invoice class
    Methods:
        setInvoiceNumber(new_number) - Set a new invoice number
        getInvoiceNumber() - Get current invoice number
        setClient(client) - Set the client for this invoice
        getClient() - Get the current client
        setPaid(bool[default=True]) - Set payment status
        getPaid() - get payment status
        setPayment(payment) - sets the payment object, calls setPaid()
        getPayment() - returns the payment object
        getTotal() - returns the total of the invoice after taxes
        getSubTotal() - returns the total of the invoice before taxes
        getTaxes() - returns the total taxes to be collected
        addItem(itemName, isTaxed, itemValue) - adds an item to the invoice
        deleteItem(itemName) - deletes an item off the invoice
        getItems() - returns a list of current items
        setDate() - sets the invoice date
        getDate() - returns invoice date
        --I have yet to decide how to represent dates. I'm thinking standard day/month/year dd/mm/yyyy
    """
    def __init__(self, i_number, client=None, paid=False, total=0):
        self.invoiceNumber = i_number
        self.client = client # To be filled by client object
        self.paid = paid # boolean asking Is it paid???
        self.total = total # running total. Probably unessisary because I have a getter.
        self.items = list() # list of tuples containing (itemName, isTaxed, value)
        self.payment = None # to be filled with a payment object
        self.date = None
    def setInvoiceNumber(self, new_number):
        self.invoiceNumber = new_number
    def getInvoiceNumber(self):
        return self.invoiceNumber
    def setClient(self, new_client):
        self.client = new_client
    def getClient(self):
        return self.client
    #the paid functions simply return if the invoice is paid
    def setPaid(self, isPaid=True):
        self.paid = isPaid
    def isPaid(self):
        return self.paid
    #the payment functions return the payment object associated
    def setPayment(self, payment):
        self.payment = payment
        if payment.howMuch() == self.getTotal():
            self.setPaid()
    def getPayment(self):
        return self.payment
    def getTotal(self):
        if len(self.items) == 0:
            raise Exception("Need items to calculate a total")
        else:
            self.total = 0
            for i in self.items:
                if(i[1] == True):
                    self.total += i[2] + (i[2]*TAX_RATE)
                else:
                    self.total += i[2]
            return round(self.total, 2)
    def getSubTotal(self):
        if len(self.items) == 0:
            raise Exception("Need items to calculate a total")
        else:
            subtotal = 0
            for i in self.items:
               subtotal += i[2]
            return subtotal
    def getTaxes(self):
        if len(self.items) == 0:
            raise Exception("Need items to calculate a total")
        else:
            taxes = 0
            for i in self.items:
                if i[1] == True:
                    taxes += i[2] * TAX_RATE
            return taxes
    def addItem(self, itemName, isTaxed, itemValue):
        if(isTaxed != None):
            self.items.append((str(itemName), isTaxed, int(itemValue)))
        else:
            raise Exception("Tax status required")
    def deleteItem(self, itemName):
        for i in range(len(self.items)):
            if self.items[i][0] == itemName:
                del self.items[i]
                break
    def getItems(self):
        return self.items.copy()
    def getDate(self):
        return self.date
    def setDate(self, date):
        self.date = date

        

class Book(object):
    """
    Book class
    represents a company's "book"
    methods:
        addInvoice(Invoice object) - adds an Invoice object to the companie's invoice db
        deleteInvoice(invoice number) - Deletes the invoice in the db
        getInvoice(invoice number) - gets invoice by number. returns invoice object
        getInvoiceByName(customer name) - returns list of invoices with said name ====================================== << to be implemented
        getInvoices(date=all) - returns all invoices in invoice db (from date onward. Default is all)
        getPaids(date=all) - returns paid invoices (from date onward. Default is all)
        getPaidsTotal(date=all) - returns total of paid invoices (from date onward. Default is all)
        getUnpaids(date=all) - returns unpaid invoice(from date onward. Default is all)
        getUnpaidTotal(date=all) - returns total of unpaid invoices (from date onward. Default is all)
        getCompanyName() - returns book name
    """
    def __init__(self, companyName):
        self.company = companyName
        self.invoices = list()
        self.clients = list()
    def _parseInvoicesByDate(self, date):
        """
        returns a list of invoices parsed by date
        date = string of dd/mm/yyyy
        !For internal use only!
        """
        #intify for comparisons. [day, month, year]
        retList = list()
        splitDate = date.split("/")
        for i in range(len(splitDate)):
            splitDate[i] = int(splitDate[i])
        for i in self.invoices:
            invDate = i.getDate().split("/")
            invDate = [int(invDate[0]), int(invDate[1]), int(invDate[2])]
            if invDate[2] >= splitDate[2]:
                if invDate[1] >= splitDate[1]:
                    if invDate[0] >= splitDate[0]:
                        retList.append(i)
        return retList
    def addInvoice(self, invoice):
        self.invoices.append(invoice)
    def deleteInvoice(self, invoiceNumber):
        for i in range(len(self.invoices)):
            if self.invoices[i].getInvoiceNumber() == invoiceNumber:
                del self.invoices[i]
                return True
        return False
    def getInvoice(self, invoiceNumber):
        for i in self.invoices:
            if i.getInvoiceNumber() == invoiceNumber:
                return i
        return False
    def getInvoices(self, date="all"):
        if date != "all":
            return self._parseInvoicesByDate(date)
        else:
            return self.invoices.copy()
    def getPaids(self, date="all"):
        if date == "all":
            paidInvoices = list()
            for i in self.invoices:
                if i.isPaid():
                    paidInvoices.append(i)
            return paidInvoices
        else:
            parsedInvoices = self._parseInvoicesByDate(date)
            paidInvoices = list()
            for i in parsedInvoices:
                if i.isPaid():
                    paidInvoices.append(i)
            return paidInvoices
    def getPaidsTotal(self, date="all"):
        if date == "all":
            total = 0
            for i in self.invoices:
                if i.isPaid():
                    total += i.getTotal()
            return total
        else:
            total = 0
            for i in self._parseInvoicesByDate(date):
                if i.isPaid():
                    total += i.getTotal()
            return total
    def getUnpaids(self, date="all"):
        if date == "all":
            unpaidInvoices = list()
            for i in self.invoices:
                if not i.isPaid():
                    unpaidInvoices.append(i)
            return unpaidInvoices
        else:
            parsedInvoices = self._parseInvoicesByDate(date)
            unpaidInvoices = list()
            for i in parsedInvoices:
                if not i.isPaid():
                    unpaidInvoices.append(i)
            return unpaidInvoices
    def getUnpaidTotal(self, date="all"):
        if date == "all":
            total = 0
            for i in self.invoices:
                if not i.isPaid():
                    total += i.getTotal()
            return total
        else:
            total = 0
            for i in self._parseInvoicesByDate(date):
                if not i.isPaid():
                    total += i.getTotal()
            return total
    def getCompanyName(self):
        return self.company

def test_functions():
    inv = Invoice(1)
    inv.setDate("22/10/2017")
    inv.addItem("service call", False, 70)
    inv.addItem("rekey", False, 12)
    inv.addItem("rekey", False, 12)
    inv.addItem("kwickset deadbolt", True, 28)
    print("Items: ", inv.getItems())
    print("Subtotal:", inv.getSubTotal())
    print("Tax", inv.getTaxes())
    print("Total", inv.getTotal())
    print("Removing the deadbolt")
    inv.deleteItem("kwickset deadbolt")
    print("Items: ", inv.getItems())
    print("Subtotal:", inv.getSubTotal())
    print("Tax", inv.getTaxes())
    print("Total", inv.getTotal())
    print("Is it paid? ", inv.isPaid())
    print("Making client")
    inv.setClient(Client("ABC Corp."))
    inv.client.address = "123 Main St."
    inv.client.phone1 = "7654321"
    inv.client.email = "abcbilling@abccorp.com"
    print("Adding a payment")
    inv.setPayment(Payment("check", 94, inv.client, "23/10/2017", paymentID="5152"))
    print("Is it paid? ", inv.isPaid())
    print("Who paid? ", inv.getPayment().whoPaid().name)
    print("How? ", inv.getPayment().method())
    print("Creating company book and adding above invoice")
        
    b = Book("Lockman Inc.")
    b.addInvoice(inv)
    
    inv = Invoice(2)
    inv.setDate("23/10/2017")
    inv.addItem("service call", False, 70)
    inv.addItem("rekey", False, 12)
    inv.addItem("rekey", False, 12)
    inv.addItem("kwickset deadbolt", True, 28)
    print("Items: ", inv.getItems())
    print("Subtotal:", inv.getSubTotal())
    print("Tax", inv.getTaxes())
    print("Total", inv.getTotal())
    print("Making client")
    inv.setClient(Client("Beth Carter"))
    inv.client.address = "77742 Juniper Ave."
    inv.client.phone1 = "1234567"
    inv.client.email = "betc@yahooper.net"
    print("Adding a payment")
    inv.setPayment(Payment("Visa", 124.17 , inv.client, "24/10/2017", paymentID="515sdg23415sd"))
    print("Is it paid? ", inv.isPaid())
    print("Who paid? ", inv.getPayment().whoPaid().name)
    print("How? ", inv.getPayment().method())
    
    print("Adding the above invoice to the ", b.getCompanyName(), "book")
    b.addInvoice(inv)
    print(b.getInvoices())
    print(b.getInvoices(date="23/10/2017"))
    print(b.getInvoice(2))
    print(b.getPaidsTotal())
    print(b.getUnpaidTotal())
    print(b.getInvoice(2).getItems())


if __name__ == "__main__":
    test_functions()


"""
Copyright (c) 2017, Tristan Henning
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.
"""