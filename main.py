from requests import get
from json import loads
import time
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpBinary, PULP_CBC_CMD

def getLands(list):
    # True Duals -> Fetch Lands -> Shock Lands -> Battle-Bond -> Cycle Horizon -> Pain -> Check -> Channels -> Pathways -> Filter (F) -> Fast -> Slow -> Triland (T) -> 
    colorIdentity = ""
    for color in colors:
        colorIdentity += color

    if (colorCount >= 2):
        search = f"commander:{colorIdentity} (game:paper) sort:usd 'Command Tower' OR 'City of Brass' OR 'Mana Confluence' OR 'Reflecting Pool' OR 'Exotic Orchard'"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), -1]

    print("Duals", end='', flush=True)
    if (budget > 320): # DUAL LANDS | DON'T EVEN CONSIDER UNLESS BUDGET IS GREATER THAN $500
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:dual"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 0]
    print(" - Done!")
    
    print("Fetches", end='', flush=True)
    if (budget > 20): # FETCH LANDS | DON'T EVEN CONSIDER UNLESS BUDGET IS GREATER THAN $20 
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:fetch-land"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    if (fetchesOutsideCID == 1):
                        if (red == 1 and (card['name'] == 'Scalding Tarn' or card['name'] == 'Arid Mesa' or card['name'] == 'Wooded Foothills' or card['name'] == 'Bloodstained Mire')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (blue == 1 and (card['name'] == 'Scalding Tarn' or card['name'] == 'Misty Rainforest' or card['name'] == 'Polluted Delta' or card['name'] == 'Flooded Strand')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (white == 1 and (card['name'] == 'Arid Mesa' or card['name'] == 'Marsh Flats' or card['name'] == 'Flooded Strand' or card['name'] == 'Windswept Heath')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (black == 1 and (card['name'] == 'Verdant Catacombs' or card['name'] == 'Marsh Flats' or card['name'] == 'Polluted Delta' or card['name'] == 'Bloodstained Mire')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (green == 1 and (card['name'] == 'Misty Rainforest' or card['name'] == 'Verdant Catacombs' or card['name'] == 'Wooded Foothills' or card['name'] == 'Windswept Heath')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                    else:
                        if (red == 1 and white == 1 and (card['name'] == 'Arid Mesa')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (red == 1 and black == 1 and (card['name'] == 'Bloodstained Mire')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (white == 1 and blue == 1 and (card['name'] == 'Flooded Strand')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (white == 1 and black == 1 and (card['name'] == 'Marsh Flats')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (green == 1 and blue == 1 and (card['name'] == 'Misty Rainforest')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (blue == 1 and black == 1 and (card['name'] == 'Polluted Delta')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (blue == 1 and red == 1 and (card['name'] == 'Scalding Tarn')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (black == 1 and green == 1 and (card['name'] == 'Verdant Catacombs')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (green == 1 and white == 1 and (card['name'] == 'Windswept Heath')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
                        if (red == 1 and green == 1 and (card['name'] == 'Wooded Foothills')):
                            list[card['name']] = [float(card['prices']['usd']), 1]
                            continue
    print(" - Done!")
    
    print("Shocks", end='', flush=True)
    if (budget > 20): # SHOCK LANDS | DON'T EVEN CONSIDER UNLESS BUDGET IS GREATER THAN $20
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:shock-land"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 2]
    print(" - Done!")

    print("Battle Bonds", end='', flush=True)
    if (budget > 20): # BATTLE BOND LANDS | DON'T EVEN CONSIDER UNLESS BUDGET IS GREATER THAN $20
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:battle-bond-land"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 3]
    print(" - Done!")

    print("Horizons", end='', flush=True)
    search = f"commander:{colorIdentity} (game:paper) sort:usd is:horizon-land" # HORIZON LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 4]
    print(" - Done!")

    print("Verges", end='', flush=True)
    search = f"commander:{colorIdentity} otag:cycle-dsk-verge (game:paper) OR commander:{colorIdentity} (game:paper) sort:usd Verge type:land set:dft" # VERGE LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 4]
    print(" - Done!")

    print("Pains", end='', flush=True)
    search = f"commander:{colorIdentity} (game:paper) sort:usd is:pain-land" # PAIN LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 5]
    print(" - Done!")

    print("Checks", end='', flush=True)
    search = f"commander:{colorIdentity} (game:paper) sort:usd is:check-land" # CHECK LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 6]
    print(" - Done!")

    print("Surveils", end='', flush=True)
    if (tappedLands == 1):
        search = f"commander:{colorIdentity} (game:paper) sort:usd o:surveil t:land r:rare o:'tapped'" # SURVEIL LANDS
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget and (card['name'] != 'Crystal Quarry')and (card['name'] != 'Cascading Cataracts')):
                    list[card['name']] = [float(card['prices']['usd']), 6]
    print(" - Done!")
    
    print("Channels", end='', flush=True)
    search = f"commander:{colorIdentity} (game:paper) sort:usd oracle:channel type:land" # CHANNEL LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 7]
    print(" - Done!")
    
    if (landCount == 2):
        print("Pathways", end='', flush=True)
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:pathway" # PATHWAY LANDS
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 8]
        print(" - Done!")
        
    print("Filters", end='', flush=True)
    if (filterLands == 1):
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:filter-land" # FILTER LANDS
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget and (card['name'] != 'Crystal Quarry')and (card['name'] != 'Cascading Cataracts')):
                    list[card['name']] = [float(card['prices']['usd']), 9]
    print(" - Done!")

    print("Scrys", end='', flush=True)
    if (tappedLands == 1):
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:scryland" # SCRY LANDS
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget and (card['name'] != 'Crystal Quarry')and (card['name'] != 'Cascading Cataracts')):
                    list[card['name']] = [float(card['prices']['usd']), 9]
    print(" - Done!")
        
    print("Fasts", end='', flush=True)
    search = f"commander:{colorIdentity} (game:paper) sort:usd is:fast-land" # FAST LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 10]
    print(" - Done!")

    print("Triomes", end='', flush=True)
    if (landCount >= 3 and tappedLands == 1):
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:triome" # FAST LANDS
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 10]
        search = f"commander:{colorIdentity} (game:paper) sort:usd is:triland" # FAST LANDS
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 9]
    print(" - Done!")

    print("Pain MDFC Lands", end='', flush=True)
    search = f"commander:{colorIdentity} (game:paper) sort:usd oracle:'you may pay 3 life' type:land (game:paper)" # PAIN MDFC LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 10]
    print(" - Done!")
        
    print("Slows", end='', flush=True)
    search = f"commander:{colorIdentity} (game:paper) sort:usd is:slow-land" # SLOW LANDS
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 11]
    print(" - Done!")

    print("Other Lands", end='', flush=True)

    if (colorCount == 1):
        search = f"commander:{colorIdentity} (oracle:'tapped unless' oracle:, oracle:untapped) type:land (game:paper) sort:usd"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 6]
    if (colorCount <= 2):
        search = f"commander:{colorIdentity} type:land castle set:ELD (game:paper) sort:usd"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 10]
    search = f"commander:{colorIdentity} Shifting Woodland"
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 7]
    search = f"commander:{colorIdentity} Shinka, the Bloodsoaked Keep"
    temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
    if (temp['object'] != "error"):
        temp = temp['data']
        for card in temp:
            if (float(card['prices']['usd']) < budget):
                list[card['name']] = [float(card['prices']['usd']), 9]
    if (tappedLands == 1):
        search = f"commander:{colorIdentity} Bojuka Bog"
        temp = loads(get(f"https://api.scryfall.com/cards/search?q={search}").text)
        if (temp['object'] != "error"):
            temp = temp['data']
            for card in temp:
                if (float(card['prices']['usd']) < budget):
                    list[card['name']] = [float(card['prices']['usd']), 4]

    print(" - Done!")
    
    return

print("Welcome to the MTG Mana Helper Application! Enter your desired use case below (number).\n 1. Given a number of lands and a budget, generate a mana base.\n 2. Insert a deck and calculate the number of lands recommended to hit mana curve.")
response = input("Response: ")

match response:
    case "1":
        # Generate Mana Base
        red, blue, green, black, white = 0, 0, 0, 0, 0
        colorCount = 0

        colors = [color for color in input("Input the colors of your deck in any order separated by space. For example, Grixis would be 'U B R': ").split()]
        for color in colors:
            match color:
                case "R":
                    red = 1
                    colorCount += 1
                case "U":
                    blue = 1
                    colorCount += 1
                case "G":
                    green = 1
                    colorCount += 1
                case "B":
                    black = 1
                    colorCount += 1
                case "W":
                    white = 1
                    colorCount += 1
                case _:
                    print(f"ERROR: {color} is not a color.")
                    quit()
        
        landCount = int(input("Now input the number of lands you would like to have in your deck: "))
        budget = float(input("Now input the budget of your mana base: $"))

        tappedLands = input("Are you okay with having unconditional tapped lands (Scry/Surveil/Gain/Etc.)? (Y/N): ")
        if (tappedLands == "Y"):
            tappedLands = 1
        else:
            tappedLands = 0

        filterLands = input("Are you okay with having filter lands? (Y/N): ")
        if (filterLands == "Y"):
            filterLands = 1
        else:
            filterLands = 0

        fetchesOutsideCID = input("Are you okay with having fetches outside of your color identity? (Y/N): ")
        if (fetchesOutsideCID == "Y"):
            fetchesOutsideCID = 1
        else:
            fetchesOutsideCID = 0

        # End of Data Gathering

        print("\nGetting Lands from Scryfall API...")

        landsCache = {}
        getLands(landsCache)

        print("Done!\n")

        '''
        print("Total Lands:\n")

        for name, data in landsCache.items():
            print(f"{name} - Value: {data[1]}, Price: {data[0]}")
        
        print("")
        '''


        print("Optimizing Lands...")
        # This optimization is a variant of an 0/1 knapsack problem, fitting as many valuable items into a sack with a certain weight capacity as you can.

        prob = LpProblem("Magic_Land_Optimizer", LpMaximize)

        # Create binary decision variables (1 if land is chosen, 0 otherwise)
        land_vars = {name: LpVariable(name, cat=LpBinary) for name, data in landsCache.items()}

        weightValue = 0.1
        weightNumber = 0.9
        prob += lpSum((((weightValue * (12 - data[1])) * land_vars[name]) + (weightNumber * land_vars[name])) for name, data in landsCache.items()), "Total_Value" # Maximize value of cards.

        prob += lpSum(data[0] * land_vars[name] for name, data in landsCache.items()) <= budget, "Total_Cost" # Prevent cost from overtaking budget
        prob += lpSum(land_vars[name] for name, data in landsCache.items()) <= landCount - colorCount, "Land_Count" # Set Land Count limit allowing for 1 basic per color minimum

        prob.solve(PULP_CBC_CMD(msg=False))

        count = 0
        print("Selected Lands:")
        for name, data in landsCache.items():
            if land_vars[name].varValue == 1:
                count += 1
                print(f"  {name} (Price: {data[0]})")
        print(f"  Basics: {landCount - count}")

        with open("lands.txt", "w") as file:
            for name, data in landsCache.items():
                if land_vars[name].varValue == 1:
                    file.write(name + "\n")


        total_price = sum(data[0] for name, data in landsCache.items() if land_vars[name].varValue == 1)
        total_value = sum((12 - data[1]) for name, data in landsCache.items() if land_vars[name].varValue == 1)

        print(f"\nTotal Price: {total_price}")
        # print(f"Total Value: {total_value}")
        # print(f"Total Count: {count}\n")
                
    case "2":
        # Calculate Land Count
        print("Create a file called 'deck.txt' and paste your Moxfield deck in there. Export your deck in Moxfield with 'MGTO' settings. It should look like this:\n1 Llanowar Elves\n1 Game of Chaos\n...")
        input("When you are done, press enter.\n")

        cards = {}

        with open('deck.txt', 'r') as file:
            for line in file:
                if (line.replace('\n', '').replace('\r', '') == ""):
                    continue
                line = line.replace('\n', '').replace('\r', '') # Remove newline
                num = int(line.split(" ", 1)[0])
                card = line.split(" ", 1)[1]
                cards[card] = num
                # print(f"{num}: {card}")
        
        totalCMC, spellCount, averageCMC, red, white, blue, black, green, colorless, progress = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        
        for name, number in cards.items():
            temp = loads(get(f"https://api.scryfall.com/cards/search?q=!\"{name}\"").text)
            if (temp['object'] != "error"):
                temp = temp['data']
                for card in temp:
                    progress += 100/len(cards.items())
                    if (card["type_line"].split(" ", 1)[0] == "Land"):
                        continue
                    elif (len(card["type_line"].split(" ", 1)) > 1):
                        if (card["type_line"].split(" ", 1)[1].split(" ", 1)[0] == "Land"):
                            continue
                    totalCMC += number * card["cmc"]
                    if (card["layout"] == "modal_dfc" or card["layout"] == "transform"):
                        card = card["card_faces"][0]
                    red += (card["mana_cost"].count(f"{{R}}") + card["mana_cost"].count(f"{{R/") + card["mana_cost"].count(f"/R}}")) * number
                    blue += (card["mana_cost"].count(f"{{U}}") + card["mana_cost"].count(f"{{U/") + card["mana_cost"].count(f"/U}}")) * number
                    white += (card["mana_cost"].count(f"{{W}}") + card["mana_cost"].count(f"{{W/") + card["mana_cost"].count(f"/W}}")) * number
                    green += (card["mana_cost"].count(f"{{G}}") + card["mana_cost"].count(f"{{G/") + card["mana_cost"].count(f"/G}}")) * number
                    black += (card["mana_cost"].count(f"{{B}}") + card["mana_cost"].count(f"{{B/") + card["mana_cost"].count(f"/B}}")) * number
                    colorless += (card["mana_cost"].count(f"{{C}}") + card["mana_cost"].count(f"{{C/") + card["mana_cost"].count(f"/C}}")) * number
                    spellCount += number
                    
                    print(f'Progress: {int(progress)}%', end='\r', flush=True)

        averageCMC = float(totalCMC / spellCount)
        print(f"Done!                 \n\nTotal CMC: {totalCMC}", flush=True)
        print(f"Spell Count: {spellCount}")
        print(f"Average CMC: {averageCMC}")
        print("\nMana:")
        totalColored = red + blue + white + black + green + colorless
        if (red > 0):
            print(f"  Red: {red} ({int((100 * red / totalColored) + 0.5)}%)")
        if (blue > 0):
            print(f"  Blue: {blue} ({int((100 * blue / totalColored) + 0.5)}%)")
        if (white > 0):
            print(f"  White: {white} ({int((100 * white / totalColored) + 0.5)}%)")
        if (black > 0):
            print(f"  Black: {black} ({int((100 * black / totalColored) + 0.5)}%)")
        if (green > 0):
            print(f"  Green: {green} ({int((100 * green / totalColored) + 0.5)}%)")
        if (colorless > 0):
            print(f"  Colorless: {colorless} ({int((100 * colorless / totalColored) + 0.5)}%)")

        print(f"\nRecommended Number of Lands (vague and likely an overestimate):\n  Low Ramp/Draw or Landfall: {int(32.42 + (3.13 * averageCMC) - (0.28 * 7))}\n  Medium Ramp/Draw: {int(31.42 + (3.13 * averageCMC) - (0.28 * 12))}\n  High Ramp/Draw: {int(31.42 + (3.13 * averageCMC) - (0.28 * 20))}\n  cEDH: {int(29.42 + (3.13 * averageCMC) - (0.28 * 30))}")

        # NUMBER OF LANDS = TOTAL CMC * 46 / 225
        quit()
    case _:
        print("ERROR: Response should be '1' or '2'.")
        quit()