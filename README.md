# rezept

This is my attempt at a python script that produces simple and readable recipe documents for the [spacebeans](https://gitlab.com/reidrac/spacebeans) [Gemini](https://gemini.circumlunar.space/) server. I will eventually add an HTML generator as well.

Available online recipe sites often require you to fill in information that I don’t want to think about when writing the recipe, e.g. the overall time requirements. Additionally, they are bloated with cookie banners, ads, comment section etc.

I was in search of a way to write down my recipes that is not more time-consuming than the pen-and-paper approach but makes them accessible from everywhere. So my top priorities for this project are the following:

* Reduce write-overhead for each new recipe. Consequently, keep characters superfluous to the recipe to a minimum.
* Ensure that the input document itself is also perfectly readable.
* Produce simplistic and readable sites.
* Enable global design changes for recipes.

# Setup
1. Setup a spacebeans server
2. Download this github repository
3. Customize spacebeans_root, back_button and handle_multiplier in custom.py
4. Write your recipes

# Writing a recipe

This is how one of my input recipes looks like:

```
head='''title: 'Blaubeer-Muffins'
story: 'Sehr einfach zu backen. Der Muffin ist oben knusprig und innen drin luftig, weich und saftig. Die Kruste ist etwas süßer als der Rest. Ergibt 12 Muffins.'
ingredients:
     Rührteig:
          - [125, g, Butter]
          - [60, g, Zucker]
          - [2, Eier]
          - [1, Pk, Vanillezucker]
          - [1, TL, Zitronenschale]
          - [250, g, Mehl]
          - [2, TL, Backpulver]
          - [150, ml, Buttermilch]
          - [250, g, Blaubeeren]
     Streusel:
          - [130, g, Mehl]
          - [60, g, Zucker]
          - [1, Pk, Vanillezucker]
          - [110, g, Butter]
tools:
     - Muffinblech
     - Papierförmchen
     - Eisportionierer
oven_instructions: 160°C Umluft, 30 Minuten
'''

instructions='''
* Muffinblech mit Papierförmchen auslegen
* Butter, Zucker und Vanillezucker verrühren
* Hintereinander die Eier unterrühren
* Zitronenschale, Mehl und Backpulver vermischen
* Buttermilch und Mehlgemisch abwechselnd in das Buttergemisch einrühren
* Teig mit Eisportionierer in die Muffinförmchen geben
* In jeden Muffin 7 Blaubeeren drücken
* Ofen auf 160°C Umluft vorheizen
* Streuselzutaten verkneten
* Stücke abreißen und auf den Muffins verteilen
* Die Muffins 25 Minuten auf mittlerer Schiene backen
* Nach dem Backen 10 Minuten abkühlen lassen.
* Muffins mit einer leichten Drehbewegung aus dem Muffinblech herauslösen.
'''

from gemtext_recipe import print_recipe
print_recipe(head, instructions, image_filename='/bakery/images/blaubeer-muffins.jpg')
```

This will generate the following gemtext document:

=> /bakery Close the book.

# Blaubeer-Muffins

Sehr einfach zu backen. Der Muffin ist oben knusprig und innen drin luftig, weich und saftig. Die Kruste ist etwas süßer als der Rest. Ergibt 12 Muffins.

=> /bakery/images/blaubeer-muffins.jpg An image of Blaubeer-Muffins

## Zutaten (Menge: ×1)

=> [GEMINI_URL]/bakery/blaubeer-muffins/?amount Specify the amount you want to make.

### Rührteig

```Rührteig-Zutaten-Tabelle
---  --  --------------
125  g   Butter
 60  g   Zucker
  2      Eier
  1  Pk  Vanillezucker
  1  TL  Zitronenschale
250  g   Mehl
  2  TL  Backpulver
150  ml  Buttermilch
250  g   Blaubeeren
---  --  --------------
```

### Streusel

```Streusel-Zutaten-Tabelle
---  --  -------------
130  g   Mehl
 60  g   Zucker
  1  Pk  Vanillezucker
110  g   Butter
---  --  -------------
```

## Utensilien

* Muffinblech
* Papierförmchen
* Eisportionierer

## Ofeneinstellung:

⏲ 160°C Umluft, 30 Minuten

## Anweisungen

* Muffinblech mit Papierförmchen auslegen
* Butter, Zucker und Vanillezucker verrühren
* Hintereinander die Eier unterrühren
* Zitronenschale, Mehl und Backpulver vermischen
* Buttermilch und Mehlgemisch abwechselnd in das Buttergemisch einrühren
* Teig mit Eisportionierer in die Muffinförmchen geben
* In jeden Muffin 7 Blaubeeren drücken
* Ofen auf 160°C Umluft vorheizen
* Streuselzutaten verkneten
* Stücke abreißen und auf den Muffins verteilen
* Die Muffins 25 Minuten auf mittlerer Schiene backen
* Nach dem Backen 10 Minuten abkühlen lassen.
* Muffins mit einer leichten Drehbewegung aus dem Muffinblech herauslösen.

=> /bakery Close the book.
