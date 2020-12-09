import sys
import inquirer
import sqlite3
from sqlite3 import Error



def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn



def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


#Add a Recipe to the database
def addRecipe(conn):
    password = input("Admin Password:\n")

    c = conn.cursor()

    #Only Admin are able use this function
    if password == "123password":
        #Ask user for the name and price of the new drink and add them to the database
        nameCocktail = input("Enter the Name of Cocktail:\n")
        priceCocktail = input("Enter the Price of Cocktail:\n")
        c.execute('''INSERT INTO Cocktail (CocktailID, Name, Price) VALUES ((SELECT MAX(CocktailID) FROM Cocktail) + 1, ?, ?)''', (nameCocktail, priceCocktail))


        #Ask the user for the amount of ingrediants in the cocktail
        ingrediantsNum = int(input("Enter the Number of Ingrediants:\n"))
        i = 1
        #Insert each ingrediant into the database and assign them to the new cocktail
        while i <= ingrediantsNum:
            #User will enter the name of the ingrediant. If the ingrediant is not already in the database it will be added
            ingrediantCocktail = input("Enter Cocktail Ingrediant:\n")
            c.execute('''SELECT Name FROM Ingrediants WHERE Name = ?''', (ingrediantCocktail,))
            data = c.fetchall()
            if not data:
                c.execute('''INSERT INTO Ingrediants (IngrediantID, Name) VALUES ((SELECT MAX(IngrediantID) FROM Ingrediants) + 1, ?);''', (ingrediantCocktail,))
            c.execute('''INSERT INTO Ingrediants_Cocktail (IngrediantID, CocktailID) VALUES ((SELECT IngrediantID FROM Ingrediants WHERE Name = ?), (SELECT CocktailID FROM Cocktail WHERE Name = ?));''', (ingrediantCocktail, nameCocktail))
            i += 1


        #Ask the user for the amount of garnish in the cocktail
        garnishNum = int(input("Enter the Number of Garnishs:\n"))
        i = 1
        #Insert each garnish into the database and assign them to the new cocktail
        while i <= garnishNum:
            #User will enter the name of the garnish. If the garnish is not already in the database it will be added
            garnishCocktail = input("Enter Cocktail Garnish:\n")
            c.execute('''SELECT Name FROM Garnish WHERE Name = ?''', (garnishCocktail,))
            data = c.fetchall()
            if not data:
                c.execute('''INSERT INTO Garnish (GarnishID, Name) VALUES ((SELECT MAX(GarnishID) FROM Garnish) + 1, ?);''', (garnishCocktail,))
            c.execute('''INSERT INTO Garnish_Cocktail (GarnishID, CocktailID) VALUES ((SELECT GarnishID FROM Garnish WHERE Name = ?), (SELECT CocktailID FROM Cocktail WHERE Name = ?));''', (garnishCocktail, nameCocktail))
            i += 1


        #Ask the user the name of the creator of the cocktail, the bar they work at, and the location of the bar
        bartenderCocktail = input("Enter the Bartender who created the Cocktail:\n")
        barCocktail = input("Enter the name of the Bar the Bartender works at:\n")
        LocationCocktail = input("Enter the Location of the Bar:\n")
        #See if Location is in the database, if not add it
        c.execute('''SELECT Name FROM Location WHERE Name = ?''', (LocationCocktail,))
        data = c.fetchall()
        if not data:
            c.execute('''INSERT INTO Location (LocationID, Name) VALUES ((SELECT MAX(LocationID) FROM Location) + 1, ?)''', (LocationCocktail,))
        #See if Bar is in the database, if not add it
        c.execute('''SELECT Name FROM Bar WHERE Name = ?''', (barCocktail,))
        data = c.fetchall()
        if not data:
            c.execute('''INSERT INTO Bar (BarID, Name, LocationID) VALUES ((SELECT MAX(BarID) FROM Bar) + 1, ?, (SELECT LocationID FROM Location WHERE Name = ?))''', (barCocktail, LocationCocktail))
        #See if Bartender is in the database, if not add it
        c.execute('''SELECT Name FROM Bartender WHERE Name = ?''', (bartenderCocktail,))
        data = c.fetchall()
        if not data:
            c.execute('''INSERT INTO Bartender (BartenderID, Name, BarID) VALUES ((SELECT MAX(BartenderID) FROM Bartender) + 1, ?, (SELECT BarID FROM Bar WHERE Name = ?))''', (bartenderCocktail, barCocktail))
        c.execute('''UPDATE Cocktail SET BartenderID = (SELECT BartenderID FROM Bartender WHERE Name = ?) WHERE CocktailID = (SELECT CocktailID FROM Cocktail WHERE Name = ?)''', (bartenderCocktail, nameCocktail))


        #Ask the user if the cocktail requires a specific glass. If not leave as null
        questions = [
        inquirer.List('choice',
                        message="Does this Cocktail require a specific Glass",
                        choices=['Yes', 'No'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        if answers['choice'] == "Yes":
            #User will enter the name of the glass. If the glass is not already in the database it will be added
            glasswareCocktail = input("Enter the Glass for the Cocktail:\n")
            c.execute('''SELECT Name FROM Glassware WHERE Name = ?''', (glasswareCocktail,))
            data = c.fetchall()
            if not data:
                #User will enter the name of the Manufacturer. If the Manufacturer is not already in the database it will be added
                glasswareSize = input("Enter Size of the Glass:\n")
                glasswareManufacturer = input("Enter Glass Manufacturer:\n")
                c.execute('''SELECT Name FROM Manufacturer WHERE Name = ?''', (glasswareManufacturer,))
                data = c.fetchall()
                if not data:
                    c.execute('''INSERT INTO Manufacturer (ManufacturerID, Name) VALUES ((SELECT MAX(ManufacturerID) FROM Manufacturer) + 1, ?)''', (glasswareManufacturer,))
                c.execute('''INSERT INTO Glassware (GlasswareID, Name, Size, ManufacturerID) VALUES ((SELECT MAX(GlasswareID) FROM Glassware) + 1, ?, ?, (SELECT ManufacturerID FROM Manufacturer WHERE Name = ?))''', (glasswareCocktail, glasswareSize, glasswareManufacturer))
            c.execute('''UPDATE Cocktail SET GlasswareID = (SELECT GlasswareID FROM Glassware WHERE Name = ?) WHERE CocktailID = (SELECT CocktailID FROM Cocktail WHERE Name = ?)''', (glasswareCocktail, nameCocktail))
        if answers['choice'] == "No":
            glasswareCocktail = ' '
            c.execute('''UPDATE Cocktail SET GlasswareID = ? WHERE CocktailID = (SELECT CocktailID FROM Cocktail WHERE Name = ?)''', (glasswareCocktail, nameCocktail))


        #User W=will enter the recipe for the cocktail
        recipeCocktail = input("Enter Cocktail Recipe:\n")
        c.execute('''INSERT INTO Preparation (CocktailID, Recipe) VALUES ((SELECT MAX(CocktailID) FROM Preparation) + 1, ?)''', (recipeCocktail,))


        #User can enter any notes for the cocktail
        noteCocktail = input("Enter Cocktail Note:\n")
        dateCocktail = input("Enter Todays Date (YYYY-MM-DD):")
        c.execute('''INSERT INTO Notes (CocktailID, Note, BartenderID, Date) VALUES ((SELECT MAX(CocktailID) FROM Notes) + 1, ?, (SELECT BartenderID FROM Bartender WHERE Name = ?), ?)''', (noteCocktail, bartenderCocktail, dateCocktail))


    #Password was incorrect. User can try again or return to the menu
    else:
        questions = [
        inquirer.List('choice',
                        message="Incorrect! Would You Like To Try Again?",
                        choices=['Yes', 'No'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        if answers['choice'] == "Yes":
            addRecipe(conn)
        if answers['choice'] == "No":
            menu(conn)


    conn.commit()


#Edit a Recipe to the database
def editRecipe(conn):
    password = input("Admin Password:\n")

    c = conn.cursor()

    #Only Admin are able use this function
    if password == "123password":
        #Ask user what they want to edit
        questions = [
        inquirer.List('choice',
                        message="What would you like to edit?",
                        choices=['Cocktail', 'Bar', 'Bartender'],
                    ),
        ]
        answers = inquirer.prompt(questions)

        if answers['choice'] == "Bar":
            #Print the available options
            c.execute('''SELECT * FROM Bar''')
            data = c.fetchall()
            print('')
            print('{:<5} | {:<30} | {}'.format("BarID", "Name", "LocationID"))
            print('----------------------------------------------------------')
            for row in data:
                print('{:<5} | {:<30} | {}'.format(row[0], row[1], row[2]))
            print('')
            #User will pick a bar and then pick what they want to edit for the selected bar
            barChoice = int(input("Select one of the BarID's listed above:\n"))
            questions = [
            inquirer.List('choice',
                        message="What do you want to change?",
                        choices=['Name', 'LocationID'],
                    ),
            ]
            answers = inquirer.prompt(questions)
            if answers['choice'] == "Name":
                barName = input("Enter New Bar Name:\n")
                c.execute('''UPDATE Bar SET Name = ? WHERE BarID = ?''', (barName, barChoice))
            if answers['choice'] == "LocationID":
                barLocation = input("Enter New Location Name:\n")
                c.execute('''SELECT Name FROM Location WHERE Name = ?''', (barLocation))
                data = c.fetchall()
                #If location is not in the database add it
                if not data:
                    c.execute('''INSERT INTO Location (LocationID, Name) VALUES ((SELECT MAX(LocationID) FROM Location) + 1, ?)''', (barLocation,))
                c.execute('''UPDATE Bar SET LocationID = (SELECT LocationID FROM Location WHERE Name = ?) WHERE BarID = ?''', (barLocation, barChoice))

        if answers['choice'] == "Bartender":
            #Print the available options
            c.execute('''SELECT * FROM Bartender''')
            data = c.fetchall()
            print('')
            print('{:<5} | {:<30} | {}'.format("BartenderID", "Name", "BarID"))
            print('----------------------------------------------------------')
            for row in data:
                print('{:<5} | {:<30} | {}'.format(row[0], row[1], row[2]))
            print('')
            #User will pick a bartender and then pick what they want to edit for the selected bartender
            bartenderChoice = int(input("Select one of the BartenderID's listed above:\n"))
            questions = [
            inquirer.List('choice',
                        message="What do you want to change?",
                        choices=['Name', 'BarID'],
                    ),
            ]
            answers = inquirer.prompt(questions)

            if answers['choice'] == "Name":
                bartenderName = input("Enter New Bartender Name:\n")
                c.execute('''UPDATE Bartender SET Name = ? WHERE BartenderID = ?''', (bartenderName, bartenderChoice))
            
            if answers['choice'] == "BarID":
                bartenderBar = input("Enter New Bar Name:\n")
                c.execute('''SELECT Name FROM Bar WHERE Name = ?''', (bartenderBar))
                data = c.fetchall()
                #If not in the database add it
                if not data:
                    bartenderLocation = input("New Bar Detected. Please Enter the Location for this Bar")
                    c.execute('''SELECT Name FROM Location WHERE Name = ?''', (bartenderLocation))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Location (LocationID, Name) VALUES ((SELECT MAX(LocationID) FROM Location) + 1, ?)''', (bartenderLocation,))
                    c.execute('''INSERT INTO Bar (BarID, Name, LocationID) VALUES ((SELECT MAX(BarID) FROM Bar) + 1, ?, (SELECT LocationID FROM Location WHERE Name = ?))''', (bartenderBar, bartenderLocation))
                c.execute('''UPDATE Bartender SET BarID = (SELECT BarID FROM Bar WHERE Name = ?) WHERE BartenderID = ?''', (bartenderBar, barChoice))

        if answers['choice'] == "Cocktail":
            #Print the available options
            c.execute('''SELECT * FROM Cocktail''')
            data = c.fetchall()
            print('')
            print('{:<10} | {:<40} | {:<5} | {:<5} | {:<5}'.format("CocktailID", "Name", "Price", "BartenderID", "GlasswareID"))
            print('--------------------------------------------------------------------------------------------------------')
            for row in data:
                print('{:<10} | {:<40} | {:<5} | {:<5} | {:<5}'.format(row[0], row[1], row[2], row[3], row[4]))
            print('')
            #User will pick a cocktail and then pick what they want to edit for the selected cocktail
            cocktailChoice = int(input("Select one of the CocktailID's listed above:\n"))
            questions = [
            inquirer.List('choice',
                        message="What do you want to change?",
                        choices=["Name", "Price", "Bartender", "Glassware", 'Ingrediants', 'Garnish', 'Notes', 'Preparation'],
                    ),
            ]
            answers = inquirer.prompt(questions)
            if answers['choice'] == "Name":
                cocktailName = input("Enter New Cocktail Name:\n")
                c.execute('''UPDATE Cocktail SET Name = ? WHERE CocktailID = ?''', (cocktailName, cocktailChoice))
            
            if answers['choice'] == "Price":
                cocktailPrice = input("Enter New Cocktail Price:\n")
                c.execute('''UPDATE Cocktail SET Price = ? WHERE CocktailID = ?''', (cocktailPrice, cocktailChoice))
            
            if answers['choice'] == "Bartender":
                cocktailBartender = input("Enter New Cocktail Creator:\n")
                c.execute('''SELECT Name FROM Bartender WHERE Name = ?''', (cocktailBartender))
                data = c.fetchall()
                #If not in the database add it
                if not data:
                    nameBar = input("New Bartender Detected. Please Enter the Name of the Bar they are located")
                    nameLocation = input("Please Enter the Location for this Bar")
                    c.execute('''SELECT Name FROM Location WHERE Name = ?''', (nameLocation))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Location (LocationID, Name) VALUES ((SELECT MAX(LocationID) FROM Location) + 1, ?)''', (nameLocation,))
                    c.execute('''SELECT Name FROM Bar WHERE Name = ?''', (nameBar))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Bar (BarID, Name, LocationID) VALUES ((SELECT MAX(BarID) FROM Bar) + 1, ?, (SELECT LocationID FROM Location Where Name = ?))''', (nameBar, nameLocation))
                    c.execute('''INSERT INTO Bartender (BartenderID, Name, BarID) VALUES((SELECT MAX(BartenderID) FROM Bartender) + 1, ?, (SELECT BarID FROM Bar WHERE Name = ?))''', (cocktailBartender, nameBar))
                c.execute('''UPDATE Cocktail SET BartenderID = (SELECT BartenderID FROM Bartender WHERE Name = ?) WHERE CocktailID = ?''', (cocktailBartender, cocktailChoice))

            if answers['choice'] == "Glassware":
                cocktailGlassware = input("Enter New Glassware:\n")
                c.execute('''SELECT Name FROM Glassware WHERE Name = ?''', (cocktailGlassware,))
                data = c.fetchall()
                #If not in the database add it
                if not data:
                    nameGlass = input("New Glassware Detected. Please Enter the Name of the Glass")
                    sizeGlass = input("Please Enter the Size of the Glass")
                    manufacturerGlass = input("Please Enter the Manufacturer of the Glass")
                    c.execute('''SELECT Name FROM Manufacturer WHERE Name = ?''', (manufacturerGlass,))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Manufacturer (ManufacturerID, Name) VALUES ((SELECT MAX(ManufacturerID) FROM Manufacturer) + 1, ?)''', (manufacturerGlass,))
                    questions = [
                    inquirer.List('choice',
                        message="Does this Glass have an Extra Charge?",
                        choices=['Yes', 'No'],
                    ),
                    ]
                    answers = inquirer.prompt(questions)
                    if answers['choice'] == "Yes":
                        extra = input("What is the extra charge?")
                        c.execute('''INSERT INTO Glassware (GlasswareID, Name, Size, ManufacturerID, ExtraCharge) VALUES ((SELECT MAX(ManufacturerID) FROM Manufacturer) + 1, ?, ?, (SELECT ManufacturerID FROM Manufacturer WHERE Name = ?))''', (nameGlass, sizeGlass, manufacturerGlass, extra))
                    if answers['choice'] == "No":
                        c.execute('''INSERT INTO Glassware (GlasswareID, Name, Size, ManufacturerID) VALUES ((SELECT MAX(ManufacturerID) FROM Manufacturer) + 1, ?, ?, (SELECT ManufacturerID FROM Manufacturer WHERE Name = ?))''', (nameGlass, sizeGlass, manufacturerGlass))
                c.execute('''UPDATE Cocktail SET GlasswareID = (SELECT GlasswareID FROM Glassware WHERE Name = ?) WHERE CocktailID = ?''', (cocktailGlassware, cocktailChoice))

            if answers['choice'] == "Ingrediants":
                questions = [
                inquirer.List('choice',
                    message="Are you adding, changing, or removing an Ingrediant",
                    choices=['Add', 'Change', 'Remove'],
                ),
                ]
                answers = inquirer.prompt(questions)
                if answers['choice'] == "Add":
                    addIngre = input("What is the new Ingrediant?")
                    c.execute('''SELECT Name FROM Ingrediants WHERE Name = ?''', (addIngre,))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Ingrediants (IngrediantID, Name) VALUES ((SELECT MAX(IngrediantID) FROM Ingrediant) + 1, ?)''', (addIngre,))
                    c.execute('''INSERT INTO Ingrediants_Cocktail (IngrediantID, CocktailID) VALUES ((SELECT IngrediantID FROM Ingrediants WHERE Name = ?), (SELECT CocktailID FROM Cocktail WHERE Name = ?))''', (addIngre, cocktailChoice))
                
                if answers['choice'] == 'Change':
                    c.execute('''SELECT Ingrediants.Name
                                FROM Cocktail
                                INNER JOIN Ingrediants_Cocktail ON Ingrediants_Cocktail.CocktailID = Cocktail.CocktailID
                                INNER JOIN Ingrediants ON Ingrediants.IngrediantID = Ingrediants_Cocktail.IngrediantID
                                WHERE Cocktail.Name = (SELECT Name FROM Cocktail WHERE CocktailID = ?);''', (cocktailChoice,))
                    data = c.fetchall()
                    print('Ingrediants:')
                    for row in data:
                        print('    {}'.format(row[0]))
                    editIngre = input("Which ingrediant do you want to edit?")
                    newIngre = input ("What do you want to change this too?")
                    c.execute('''SELECT Name FROM Ingrediants WHERE Name = ?''', (newIngre,))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Ingrediants (IngrediantID, Name) VALUES ((SELECT MAX(IngrediantID) FROM Ingrediant) + 1, ?)''', (newIngre,))
                    c.execute('''UPDATE Ingrediants_Cocktail SET IngrediantID = (SELECT IngrediantID FROM Ingrediants WHERE Name = ?) WHERE CocktailID = ? AND IngrediantID = (SELECT IngrediantID FROM Ingrediants WHERE Name = ?)''', (newIngre, cocktailChoice, editIngre))
                
                if answers['choice'] == "Remove":
                    deleteIngre = input("Which ingrediant do you want to remove?")
                    c.execute('''DELETE FROM Ingrediants_Cocktail WHERE IngrediantID = (SELECT IngrediantID FROM Ingrediants WHERE Name = ?) AND CocktailID = ?;''', (deleteIngre, cocktailChoice))
            
            if answers['choice'] == "Garnish":
                questions = [
                inquirer.List('choice',
                    message="Are you adding, changing, or removing a Garnish",
                    choices=['Add', 'Change', 'Remove'],
                ),
                ]
                answers = inquirer.prompt(questions)
                if answers['choice'] == "Add":
                    addGarnish = input("What is the new Garnish?")
                    c.execute('''SELECT Name FROM Garnish WHERE Name = ?''', (addGarnish,))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Garnish (GarnishID, Name) VALUES ((SELECT MAX(GarnishID) FROM Garnish) + 1, ?)''', (addGarnish,))
                    c.execute('''INSERT INTO Garnish_Cocktail (GarnishID, CocktailID) VALUES ((SELECT GarnishID FROM Garnish WHERE Name = ?), (SELECT CocktailID FROM Cocktail WHERE Name = ?))''', (addGarnish, cocktailChoice))
                
                if answers['choice'] == 'Change':
                    c.execute('''SELECT Garnish.Name
                                FROM Cocktail
                                INNER JOIN Garnish_Cocktail ON Garnish_Cocktail.CocktailID = Cocktail.CocktailID
                                INNER JOIN Garnish ON Garnish.GarnishID = Garnish_Cocktail.GarnishID
                                WHERE Cocktail.Name = (SELECT Name FROM Cocktail WHERE CocktailID = ?);''', (cocktailChoice,))
                    data = c.fetchall()
                    print('Garnish:')
                    for row in data:
                        print('    {}'.format(row[0]))
                    editGarnish = input("Which Garnish do you want to edit?")
                    newGarnish = input ("What do you want to change this too?")
                    c.execute('''SELECT Name FROM Garnish WHERE Name = ?''', (newGarnish,))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        c.execute('''INSERT INTO Garnish (GarnishID, Name) VALUES ((SELECT MAX(GarnishID) FROM Garnish) + 1, ?)''', (newGarnish,))
                    c.execute('''UPDATE Garnish_Cocktail SET GarnishtID = (SELECT GarnishID FROM Garnish WHERE Name = ?) WHERE CocktailID = ? AND GarnishID = (SELECT GarnishID FROM Garnish WHERE Name = ?)''', (newGarnish, cocktailChoice, editGarnish))
                
                if answers['choice'] == "Remove":
                    deleteGarnish = input("Which Garnish do you want to remove?")
                    c.execute('''DELETE FROM Garnish_Cocktail WHERE GarnishID = (SELECT GarnishID FROM Garnish WHERE Name = ?) AND CocktailID = ?;''', (deleteGarnish, cocktailChoice))
            
            
            if answers['choice'] == "Notes":
                questions = [
                inquirer.List('choice',
                    message="What do you want to change?",
                    choices=['Note', 'BartenderID', 'Date'],
                ),
                ]
                answers = inquirer.prompt(questions)
                if answers['choice'] == "Note":
                    cocktailNote = input("Enter Notes:\n")
                    c.execute('''UPDATE Notes SET Note = ? WHERE CocktailID = ?''', (cocktailNote, cocktailChoice))
                
                if answers['choice'] == "BartenderID":
                    notesBartender = input("Enter Bartender Name:\n")
                    c.execute('''SELECT Name FROM Bartender WHERE Name = ?''', (notesBartender))
                    data = c.fetchall()
                    #If not in the database add it
                    if not data:
                        nameBar = input("New Bartender Detected. Please Enter the Name of the Bar they are located")
                        nameLocation = input("Please Enter the Location for this Bar")
                        c.execute('''SELECT Name FROM Location WHERE Name = ?''', (nameLocation))
                        data = c.fetchall()
                        #If not in the database add it
                        if not data:
                            c.execute('''INSERT INTO Location (LocationID, Name) VALUES ((SELECT MAX(LocationID) FROM Location) + 1, ?)''', (nameLocation,))
                        c.execute('''SELECT Name FROM Bar WHERE Name = ?''', (nameBar))
                        data = c.fetchall()
                        #If not in the database add it
                        if not data:
                            c.execute('''INSERT INTO Bar (BarID, Name, LocationID) VALUES ((SELECT MAX(BarID) FROM Bar) + 1, ?, (SELECT LocationID FROM Location Where Name = ?))''', (nameBar, nameLocation))
                        c.execute('''INSERT INTO Bartender (BartenderID, Name, BarID) VALUES((SELECT MAX(BartenderID) FROM Bartender) + 1, ?, (SELECT BarID FROM Bar WHERE Name = ?))''', (notesBartender, nameBar))
                    c.execute('''UPDATE Notes SET BartenderID = (SELECT BartenderID FROM Bartender WHERE Name = ?) WHERE CocktailID = ?''', (notesBartender, cocktailChoice))
                
                if answers['choice'] == "Date":
                    notesDate = input("Enter Date:\n")
                    c.execute('''UPDATE Notes SET Date = ? WHERE CocktailID = ?''', (notesDate, cocktailChoice))
                        
            if answers['choice'] == "Preparation":
                cocktailRecipe = input("Enter Recipe:\n")
                c.execute('''UPDATE Preparation SET Recipe = ? WHERE CocktailID = ?''', (cocktailRecipe, cocktailChoice))


    #Password was incorrect. User can try again or return to the menu
    else:
        questions = [
        inquirer.List('choice',
                        message="Incorrect! Would You Like To Try Again?",
                        choices=['Yes', 'No'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        if answers['choice'] == "Yes":
            editRecipe(conn)
        if answers['choice'] == "No":
            menu(conn)


    conn.commit()



#Search for a Cocktail and display its recipe
def searchRecipe(conn):
    chosenCocktail = input("Enter Cocktail Name:\n")

    c = conn.cursor()
    c.execute('''SELECT Name, Price FROM Cocktail WHERE Name = ?''', (chosenCocktail,))
    data = c.fetchall()

    #If the users input is not within the database
    if not data:
        print('')
        print('%s Was Not Found' %chosenCocktail)
        print('')

        questions = [
        inquirer.List('choice',
                        message="Select an option",
                        choices=['Try Again', 'Go Back'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        if answers['choice'] == "Try Again":
            searchRecipe(conn)
        if answers['choice'] == "Go Back":
            menu(conn)

    #Print the recipe for the selected cocktail and ask if they want to see its notes
    else:
        print('')
        for row in data:
            print('Name:\n    {}\nPrice:\n    ${}'.format(row[0], row[1]))

        #Print Ingrediants
        c.execute('''SELECT Ingrediants.Name AS Ingrediants
                    FROM Cocktail
                    INNER JOIN Ingrediants_Cocktail ON Ingrediants_Cocktail.CocktailID = Cocktail.CocktailID
                    INNER JOIN Ingrediants ON Ingrediants.IngrediantID = Ingrediants_Cocktail.IngrediantID
                    WHERE Cocktail.Name = ?;''', (chosenCocktail,))
        data = c.fetchall()
        print('Ingrediants:')
        for row in data:
            print('    {}'.format(row[0]))

        #Print Garnish
        c.execute('''SELECT Garnish.Name
                    FROM Cocktail
                    INNER JOIN Garnish_Cocktail ON Garnish_Cocktail.CocktailID = Cocktail.CocktailID
                    INNER JOIN Garnish ON Garnish.GarnishID = Garnish_Cocktail.GarnishID
                    WHERE Cocktail.Name = ?;''', (chosenCocktail,))
        data = c.fetchall()
        print('Garnish:')
        for row in data:
            print('    {}'.format(row[0]))

        #Print Glassware
        c.execute('''SELECT Glassware.Name
                    FROM Cocktail
                    INNER JOIN Glassware ON Glassware.GlasswareID = Cocktail.GlasswareID
                    WHERE Cocktail.Name = ?;''', (chosenCocktail,))
        data = c.fetchall()
        print('Glassware:')
        for row in data:
            print('    {}'.format(row[0]))
        #If Glassware is null, Customers have multiple options
        if not data:
            c.execute('''SELECT Name, Size, ExtraCharge
                        FROM Glassware
                        WHERE Name = 'Coupe' OR Name = 'Rocks Glass' OR Name = 'Collins' OR Name = 'Punch Bowl'
                        ORDER BY ExtraCharge ASC;''')
            data = c.fetchall()
            print('    Customer may choose:')
            for row in data:
                print('        Name: {:<15} Size: {:<15} Extra Charge: ${}'.format(row[0], row[1], row[2]))

        #Print Recipe
        c.execute('''SELECT Preparation.Recipe
                    FROM Cocktail
                    INNER JOIN Preparation ON Preparation.CocktailID = Cocktail.CocktailID
                    WHERE Cocktail.Name = ?;''', (chosenCocktail,))
        data = c.fetchall()
        print('Recipe:')
        for row in data:
            print('    {}\n'.format(row[0]))

        #Ask user to see notes
        questions = [
        inquirer.List('choice',
                        message="Would you like to see the notes for this cocktail",
                        choices=['Yes', 'No'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        if answers['choice'] == "Yes":
            c.execute('''SELECT Notes.Note, Bartender.Name, Notes.Date
                        FROM Notes
                        INNER JOIN Bartender ON Bartender.BartenderID = Notes.BartenderID
                        INNER JOIN Cocktail ON Cocktail.CocktailID = Notes.CocktailID
                        WHERE Cocktail.Name = ?;''', (chosenCocktail,))
            data = c.fetchall()
            if not data:
                print('No Notes Available\n')
                menu(conn)
            for row in data:
                print('Notes:\n    {}\nAuthor:\n    {}\nDate:\n    {}\n'.format(row[0], row[1], row[2]))
        if answers['choice'] == "No":
            menu(conn)



def delete(conn):
    password = input("Admin Password:\n")

    c = conn.cursor()

    #Only Admin are able use this function
    if password == "123password":
        questions = [
        inquirer.List('choice',
                        message="WARNING: Deleted data can not be recovered. Do you wish to continue?",
                        choices=['Yes', 'No'],
                    ),
        ]
        answers = inquirer.prompt(questions)

        if answers['choice'] == "Yes":
            #Ask user what they want to edit
            questions = [
            inquirer.List('choice',
                            message="Where would you like to delete from?",
                            choices=['Bar', 'Bartender', 'Cocktail', 'Garnish', 'Glassware', 'Ingrediants', 'Location', 'Manufacturer'],
                        ),
            ]
            answers = inquirer.prompt(questions)

            if answers['choice'] == "Bar":
                c.execute('''SELECT BarID, Name FROM Bar''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dBar = int(input("Enter the BarID for the Bar you want to delete\n"))
                c.execute('''DELETE FROM Bar WHERE BarID = ?''', (dBar,))

            if answers['choice'] == "Bartender":
                c.execute('''SELECT BartenderID, Name FROM Bartender''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dBartender = int(input("Enter the BartenderID for the Bartender you want to delete\n"))
                c.execute('''DELETE FROM Bartender WHERE BartenderID = ?''', (dBartender,))

            if answers['choice'] == "Cocktail":
                c.execute('''SELECT CocktailID, Name FROM Cocktail''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dCocktail = int(input("Enter the CocktailID for the Cocktail you want to delete\n"))
                c.execute('''DELETE FROM Cocktail WHERE CocktailID = ?''', (dCocktail,))
                c.execute('''DELETE FROM Ingrediants_Cocktail WHERE CocktailID = ?''', (dCocktail,))
                c.execute('''DELETE FROM Garnish_Cocktail WHERE CocktailID = ?''', (dCocktail,))
                c.execute('''DELETE FROM Notes WHERE CocktailID = ?''', (dCocktail,))
                c.execute('''DELETE FROM Preparation WHERE CocktailID = ?''', (dCocktail,))

            if answers['choice'] == "Garnish":
                c.execute('''SELECT GarnishID, Name FROM Garnish''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dGarnish = int(input("Enter the GarnishID for the Garnish you want to delete\n"))
                c.execute('''DELETE FROM Garnish WHERE GarnishID = ?''', (dGarnish,))
                c.execute('''DELETE FROM Garnish_Cocktail WHERE GarnishID = ?''', (dGarnish,))

            if answers['choice'] == "Glassware":
                c.execute('''SELECT GlasswareID, Name FROM Glassware''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dGlassware = int(input("Enter the GlasswareID for the Glassware you want to delete\n"))
                c.execute('''DELETE FROM Glassware WHERE GlasswareID = ?''', (dGlassware,))

            if answers['choice'] == "Ingrediants":
                c.execute('''SELECT IngrediantID, Name FROM Ingrediants''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dIngrediants = int(input("Enter the IngrediantID for the Ingrediants you want to delete\n"))
                c.execute('''DELETE FROM Ingrediants WHERE IngrediantID = ?''', (dIngrediants,))
                c.execute('''DELETE FROM Ingrediants_Cocktail WHERE IngrediantID = ?''', (dIngrediants,))

            if answers['choice'] == "Location":
                c.execute('''SELECT LocationID, Name FROM Location''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dLocation = int(input("Enter the LocationID for the Location you want to delete\n"))
                c.execute('''DELETE FROM Location WHERE LocationID = ?''', (dLocation,))

            if answers['choice'] == "Manufacturer":
                c.execute('''SELECT ManufacturerID, Name FROM Manufacturer''')
                data = c.fetchall()
                for row in data:
                    print('{} | {}'.format(row[0], row[1]))
                dManufacturer = int(input("Enter the ManufacturerID for the Manufacturer you want to delete\n"))
                c.execute('''DELETE FROM Manufacturer WHERE ManufacturerID = ?''', (dManufacturer,))

        if answers['choice'] == "No":
            menu(conn)

    #Password was incorrect. User can try again or return to the menu
    else:
        questions = [
        inquirer.List('choice',
                        message="Incorrect! Would You Like To Try Again?",
                        choices=['Yes', 'No'],
                    ),
        ]
        answers = inquirer.prompt(questions)
        if answers['choice'] == "Yes":
            editRecipe(conn)
        if answers['choice'] == "No":
            menu(conn)


    conn.commit()



def menu(conn):
    with conn:
        while True:
            questions = [
            inquirer.List('choice',
                            message="Select an option",
                            choices=['Edit Cocktail Recipe', 'Add Cocktail Recipe', 'Show all Cocktails', 'Search For Cocktail Recipe', 'Delete Item', 'Exit'],
                        ),
            ]
            answers = inquirer.prompt(questions)
            if answers['choice'] == "Show all Cocktails":
                c = conn.cursor()
                c.execute('''SELECT Cocktail.Name, Bartender.Name AS Creator, Bar.Name AS Bar, Location.Name AS Location
                            FROM Cocktail
                            INNER JOIN Bartender ON Bartender.BartenderID = Cocktail.BartenderID
                            INNER JOIN Bar ON Bar.BarID = Bartender.BarID
                            INNER JOIN Location ON Location.LocationID = Bar.LocationID;''')
                data = c.fetchall()
                print('')
                print('{:<40} | {:<30} | {:<30} | {}'.format("Name", "Creator", "Bar", "Location"))
                print('--------------------------------------------------------------------------------------------------------------------------------------------------')
                for row in data:
                    print('{:<40} | {:<30} | {:<30} | {}'.format(row[0], row[1], row[2], row[3]))
                print('')
            if answers['choice'] == "Add Cocktail Recipe":
                addRecipe(conn)
            if answers['choice'] == "Edit Cocktail Recipe":
                editRecipe(conn)
            if answers['choice'] == "Delete Item":
                delete(conn)
            if answers['choice'] == "Search For Cocktail Recipe":
                searchRecipe(conn)
            if answers['choice'] == "Exit":
                sys.exit(0)



def main():
    database = r"Cocktails-Updated.db"

    # create a database connection
    conn = openConnection(database)
    menu(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()

