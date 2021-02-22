# pylint: disable=missing-docstring,line-too-long
import sys
import os
import csv
from os import path
import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://recipes.lewagon.com/"

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    recipe_list = []
    for recipe in soup.find_all("div", class_="p-2 recipe-details"):
        name = recipe.find("p").string.replace('"', '')
        difficulty = recipe.find("span", class_="recipe-difficulty").string
        prep_time = recipe.find("span", class_="recipe-cooktime").string
        recipe_dict = {}
        recipe_dict['name'] = name
        recipe_dict['difficulty'] = difficulty
        recipe_dict['prep_time'] = prep_time
        recipe_list.append(recipe_dict)
    return recipe_list


def write_csv(ingredient, recipes):
    file_exists = os.path.isfile(f'recipes/{ingredient}.csv')
    with open(f'recipes/{ingredient}.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=recipes[0].keys())
        if not file_exists:
            writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient, start=0):
    response = requests.get(
        SEARCH_URL,
        params={'search[query]': ingredient, 'page': start}
        )
    return response.text

#def scrape_from_internet(ingredient, page_number):
 #   response = requests.get(f"https://recipes.lewagon.com/?search[query]={ingredient}&page={page_number}")
    #os.system(f'curl -s "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
  #  return response


def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file)
    print("Please, run the following command first:")
    print(f'curl -s "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        for i in range(3):
            #if i < 2:
            #    number = 12
            #else:
                #number = 6
            recipes = parse(scrape_from_internet(ingredient, i+1))
            write_csv(ingredient, recipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
