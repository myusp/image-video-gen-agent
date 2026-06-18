import os
import json

project_folder = "output/20260603_mindset-video"
base_style = "colorful marker sketch illustration, hand-drawn marker art, vibrant colors, clean white background, representative simple drawing, minimal text, landscape 16:9 aspect ratio"

# Visual prompts representing each scene's core idea in the requested marker style
prompts = {
    1: "A person sitting at a desk looking frustrated and tired, surrounded by stacks of papers and sticky notes.",
    2: "A welcoming host pointing at a whiteboard with the word 'MINDSET vs SYSTEM' written on it.",
    3: "Stacks of self-help and finance books piled high, with a bookmark sticking out.",
    4: "A person standing on a mountain peak feeling victorious, but it is just a dream bubble above them sleeping on a couch.",
    5: "A glowing lightbulb shining next to a confused brain icon, simple and clean.",
    6: "An open book with colorful rainbows, stars, and clouds coming out of its pages, looking artificial.",
    7: "A street merchant selling a shiny box labeled 'MOTIVATION' with empty space inside.",
    8: "Hands holding a piggy bank next to a growing green plant sprout.",
    9: "A lottery winner standing under a shower of falling money, but looking stressed as the money flies away.",
    10: "A person sitting in a cinema theater eating popcorn and watching a big screen with glowing 'MOTIVATION' text.",
    11: "An online shopping cart overflowing with boxes on a smartphone screen, simple layout.",
    12: "A structured blueprint showing gears, folders, and piggy banks connected in a system flow.",
    13: "A person holding a huge heavy book of knowledge, standing before a complex maze with no path.",
    14: "An ancient clay tablet with cuneiform writing next to ancient gold coins.",
    15: "A hand placing a coin directly into a piggy bank labeled 'ME' before paying other bills.",
    16: "A battery icon that is low and flashing red, representing exhausted willpower and decision fatigue.",
    17: "A stressed worker looking at a shopping bag labeled 'SELF REWARD' with a sad face.",
    18: "A house built on sand collapsing, compared to a house built on a strong brick foundation.",
    19: "A business owner running on a giant hamster wheel looking exhausted, representing a job.",
    20: "A mechanical engine with gears turning automatically to process falling gold coins.",
    21: "A person manually juggling multiple bills and credit cards with a stressed expression.",
    22: "A person sleeping peacefully in a comfortable bed while coins are automatically sorted into folders.",
    23: "A fast-food kitchen with a conveyor belt preparing burgers perfectly, representing a franchise.",
    24: "A computer screen showing an automated pipeline with arrows moving coins from paycheck to savings.",
    25: "A pie chart showing paycheck split: 50% fixed costs, 10% investment, 10% emergency, 30% fun.",
    26: "An arrow pointing from a bank vault to a growth chart with a green line rising.",
    27: "A happy person drinking a cup of coffee at a cafe, holding a phone showing a digital banking app.",
    28: "A smartphone screen showing a digital bank interface with multiple colorful pockets labeled 'Bills', 'Invest', 'Travel'.",
    29: "A large, stylized thumbs-up 'Like' button in a colorful marker style.",
    30: "A scale with a glowing brain labeled 'MINDSET' on one side and a machine gear labeled 'SYSTEM' on the other, perfectly balanced.",
    31: "A compass pointing the way, sitting next to a running mechanical engine with gears.",
    32: "Two paths splitting: Path A is messy and uphill, Path B is a smooth conveyor belt.",
    33: "A person sweating, manually entering bank details on a phone while looking at a calendar.",
    34: "A pile of gold coins growing exponentially like a mountain over time.",
    35: "Coins evaporating into thin clouds, with a person looking confused and empty-handed.",
    36: "A person sitting in a counseling chair with a brain icon, while another side shows hands assembling a gear mechanism.",
    37: "A finger pressing an 'Enable Auto-Debit' toggle button on a mobile banking application.",
    38: "A person staring at a wall covered with 'THINK POSITIVE' sticky notes, looking empty-handed.",
    39: "A complex spreadsheet table on a computer screen starting to crack and break under pressure.",
    40: "A puzzle piece of a brain connecting perfectly with a puzzle piece of a gear.",
    41: "A calendar with checkmarks on every day, representing consistent action.",
    42: "A television showing an action movie with explosions, while a viewer sits passively on a couch.",
    43: "A colorful marker drawing of a 'Subscribe' button with a bell notification icon next to it.",
    44: "A person standing in front of a giant blueprints board, drawing a financial machine that operates automatically."
}

for i in range(1, 45):
    scene_dir = os.path.join(project_folder, f"scene_{i}")
    os.makedirs(scene_dir, exist_ok=True)
    prompt_file = os.path.join(scene_dir, f"prompt_{i}.txt")
    
    scene_prompt = prompts.get(i, "A representative drawing of financial management.")
    full_prompt = f"A {scene_prompt} {base_style}"
    
    with open(prompt_file, "w") as f:
        f.write(full_prompt)
        
print(f"Successfully generated 44 prompts in {project_folder}!")
