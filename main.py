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

from classes import *
import parsingFunctions as parsing


def main():
    #depickle instances into lists
    book_list = list()
    
    print("Welcome to ITrack, the terminal based invoice tracker. Type HELP at any point to get help.")
    print("ITrack is a free project maintained in my spare time. Don't expect it to work the way it should or be supported all of the time.")
    print("ITrack is free software licenced under the BSD Licence. This is a very permissive licence. Do what you wish with this software.")
    if len(book_list) < 1:
        print("\nNo books detected. Creating a new book.")
        cname = input("Company Name? ")
        book_list.append(Book(cname))
    
    print("Please select a book: ")
    j = 0
    for i in book_list:
        print(j, " : ", i.getCompanyName())
        j += 1
    pick = input("Please enter the number of the book you wish to start editing: ")
    current_book = book_list[int(pick)]
    print("T! Current Book = ", current_book.getCompanyName())
    while True:
        cmd = input(">>> ")
        parsing.parser(cmd)

if __name__ == "__main__":
    main()






































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