"""
Grocery List Compiler
by Gustavo Rivero
V 1.0.0 completed on 06/02/2023

this program reads recipe ingredient lists from csv files saved in the "recipes" directory and prompts the user
to select their chosen recipes.

Once the user selects a recipe or more, the program compiles a list of all recipe ingredients and calculates the total
necessary quantity of ingredients needed for all recipes into a txt file for a faster shopping experience
"""
import csv
import os

import inquirer


def main():
    # Prompt user for list of wanted recipes
    recipes = prompt_user_for_recipes()

    # extract ingredients per recipe
    ingredients_list = []  # init empty list of ingredients
    for recipe in recipes:  # for each recipe,
        ingredients_list.append(extract_recipe_ingredients(recipe))  # add the list of ingredients to the master list

    # compile ingredients list
    compiled_list = compile_ingredients_list(ingredients_list)
    grocery_list = display_consolidated_list(compiled_list)
    print(grocery_list)

    # export shopping list into a txt file
    create_grocery_list_file(grocery_list)


def prompt_user_for_recipes():
    """Prompts user for recipes from available list and returns a list of selected recipes"""
    # load all recipe files into a compiled list of options
    recipes_files = os.listdir("recipes")  # read all recipe csv files
    recipes = []  # init empty recipes option list
    for recipe in recipes_files:
        recipes.append(display_recipe_name(recipe))  # save recipes to option list with english names

    # Define the list of options based on loaded data
    options = [
        inquirer.Checkbox('options',
                          message='Select options - Spacebar to Select/Enter to Confirm List',
                          choices=recipes)
    ]

    # Prompt the user to select options
    answers = inquirer.prompt(options)

    # Return the selected options
    return answers['options']


def extract_recipe_ingredients(recipe):
    """Extracts the ingredients list from a recipe"""
    ingredients = []

    with open(get_recipe_file_name(recipe)) as file:
        # this method prevents assuming order of columns
        reader = csv.DictReader(file)  # returns a list of dictionary based on the csv files separated by rows
        for row in reader:
            ingredients.append(
                {
                    # key names taken from first row of csv file
                    "quantity": row['quantity'],
                    "denomination": row['denomination'],
                    "ingredient": row['ingredient']
                })

    return ingredients


def compile_ingredients_list(ingredients_list):
    """Compiles all similar ingredients and their quantities into a consolidated master shopping list"""
    ingredient_history = []  # init empty history list
    compiled_ingredients_list = []  # init empty compiled list

    for ingredients in ingredients_list:  # search all recipes,
        for ingredient_item in ingredients:  # search all ingredients in each recipe,

            # extract individual values
            quantity = ingredient_item["quantity"]
            denomination = ingredient_item["denomination"]
            ingredient = ingredient_item["ingredient"]

            # Consolidate
            if ingredient not in ingredient_history:  # If ingredient has not been entered into history,
                ingredient_history.append(ingredient)  # add to history log,
                compiled_ingredients_list.append(ingredient_item)  # add details to compiled list
            else:  # if ingredient is a duplicate,
                for ingredient_line in compiled_ingredients_list:  # iterate through compiled list
                    if ingredient == ingredient_line['ingredient']:  # and search for the right ingredient
                        if quantity == "*":  # if ingredient does not specify quantity, continue
                            continue
                        else:  # if ingredient expresses a certain quantity
                            if ingredient_line["quantity"] == "*":
                                # some ingredients may specify qty in some recipes but not others.
                                # this if statement sets unspecified qty to 0 if it was unspecified before
                                # and adds the denomination
                                ingredient_line["quantity"] = 0
                                ingredient_line["denomination"] = denomination
                            new_quantity = float(ingredient_line["quantity"]) + float(quantity)  # add float values,
                            ingredient_line["quantity"] = str(new_quantity)  # save new quantity as str

    return compiled_ingredients_list


def display_consolidated_list(consolidated_data):
    """Returns an easy-to-read string of the entire recipes shopping list"""
    shopping_list = ""

    for line in consolidated_data:
        if line["quantity"] == "*":
            shopping_list += f"[ ] {line['ingredient']}\n"
        elif line["denomination"] == "*":
            shopping_list += f"[ ] {line['quantity']} {line['ingredient']}\n"
        else:
            shopping_list += f"[ ] {line['quantity']} {line['denomination']} of {line['ingredient']}\n"

    return shopping_list


def create_grocery_list_file(grocery_list):
    """Creates a .txt file of the grocery list"""
    # Open the file in write mode
    file = open("grocery_list.txt", "w")

    # Write the string to the file
    file.write(grocery_list)

    # Close the file
    file.close()


def display_recipe_name(filename):
    """Turns file name from the Recipes dir into a proper english recipe name"""
    return filename[:-4].replace("_", " ").title()


def get_recipe_file_name(recipe):
    """Returns the filename of a given recipe"""
    return "recipes/" + recipe.replace(" ", "_").lower() + ".csv"


if __name__ == "__main__":
    main()
