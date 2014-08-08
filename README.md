flashcard
=========

a pythonista script for displaying flashcards

There are two versions here.  

Flashcard.py - a flashcard training program, using the Hydrogen gui.,  This is for reference purposes and is now obsolete

flashcard_UI.py - the enhanced version utilizing the new ui interface in pythonista version 1.5
Flashcard_UI.pyui is the main View definiton
Flash_Dict.pyui   is the Dictionaly View definitions

Flashcards are image files ('png or jpg) stored in a heirarchical file system within the pythonista file structure.  The 
individual image files are organized in "chapter folders", and those in a "book" folder.  In the files here, the book folder
is ASL (I am studying sign language). 

The filename becomes a decriptor.  An image can have multiple descriptors.  To accomplish this, the filename is a comma
separated list of descriptors.  When sorting these descriptor for the dictionary view (see below), noise words (the, a, to, to be)
are ignored.  

In flashcard mode, the user selects which chapter(s) will be displayed.  The user chooses whether the image, its descriptor, 
either randomly, or both are displayed.  The user must answer before moving to the next image.  

In dictionary mode, a list of all descriptos are given in alphabetical order.  A "jump" index is display to allow to move to 
fast through the list.


