from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def makerows(row):
    """
    This is just to show a bit of string manipulation and list handling.
    Will build a string of everything until the first digit is encountered.
    Then builds a list with that and a split (on empty) of the rest of the row.
    * = unpack (unpacks list into individual elements
        Used to avoid creating a temp, throw-away variable
    :param row: current row of table (as full string)
    :return: list of Statical description(str), Team(str,int,float), and Opponents(str,int,float)
    """

    words = ""

    for i, letter in enumerate(row):
        if not letter.isdigit():
            words += letter
        else:
            return [words.strip(), *row[i:].split(" ")]

"""
Basic overview of selenium over Beautiful Soup for webscrapping.
Loads multiple select options of a table then grabs the data.
Not optimized (good candidate for moving to async or multiprocess with bots)
"""
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://fgcuathletics.com/sports/womens-soccer/stats/2022")
    assert "Page not found" not in driver.page_source

    mostgame={

        }
    # To get the first five - a simple loop. You could add that threading here
    for i in range(1, 4):



        # Get select option by index to make less weak
        selects = Select(driver.find_element(By.XPATH, "//select"))
        selects.select_by_index(i)

        #select game by game, game by game, our offensive stat

        driver.find_element(By.XPATH, "//a[@href='#game']").click()


        driver.find_element(By.XPATH, "//a[@href='#game-game']").click()
       
        driver.find_element(By.XPATH, "//a[@href='#game-game-our-offensive']").click()



        year = 2023 - i
        print(year)

        table_rows = []

        table_data = driver.find_elements(By.XPATH, "//table[1]//thead//tr//th")


        table_rows.append([h.text for h in table_data if h.text])

 

        table_data = driver.find_elements(By.XPATH, "//table[1]/tbody/tr")
        for row in table_data:
            if row.text:
                cur_row = makerows(row.text)
                # if cur_row is blank it will return None so check that & length
                if cur_row is None or len(cur_row) == 1:
                    continue
                else:
                    table_rows.append(cur_row)
        countgame = len(table_rows)-1
        with open(f"{year}_sport.txt", "w", encoding="utf-8") as f:
            f.write(f"Amount of games played in {year}: {countgame}\n")

        for i, row in enumerate(table_rows):
            print(f"Row {i} is: {row}")
            with open(f"{year}_sport.txt", "a", encoding="utf-8") as f:
                f.write(f"Row {i} is: {row}\n")

        #find most game season
        mostgame.update({year: countgame})

##this must can be done in an easy way, my brain just not working now
    if mostgame.get(2022) < mostgame.get(2021):
        if mostgame.get(2022) < mostgame.get(2020):
            if mostgame.get(2021)<mostgame.get(2020):
                print(f"They did the best in season 2020")
            elif mostgame.get(2021) > mostgame.get(2020):
                print(f"They did the best in season 2021")
            elif mostgame.get(2021) == mostgame.get(2020):
                print(f"They did the best in both season 2020 and 2021")
        else:
            print(f"They did the best in season 2021")
    elif mostgame.get(2022) == mostgame.get(2021):
        if mostgame.get(2022) < mostgame.get(2020):
            print(f"They did the best in season 2020")
        elif mostgame.get(2022) == mostgame.get(2020):
            print(f"They did the best in all season 2020 and 2021 and 2022")
        else:
            print(f"They did the best in both season 2022 and 2021")
    else:
        if  mostgame.get(2022) > mostgame.get(2020):
            print(f"They did the best in season 2022")

        elif mostgame.get(2022) == mostgame.get(2020):
            print(f"They did the best in both season 2022 and 2020")



    driver.close()