def get_task_name_using_taxonomy(task_name):
    if task_name in [
        "General Cleaning",
        "Deep Cleaning",
        "Flat Cleaning",
        "Home Cleaning",
        "Organize Home",
        "Organise Home",
        "Deep Clean",
        "Back To Clean",
        "Cleaning",
        "Back To Organized",
        "Organize & Declutter",
        "Organize Closet",
    ]:
        return "General Cleaning"
    elif task_name in [
        "Run Errands",
        "Grocery Shopping",
        "Wait in Line",
        "Shop For & Install Decorations",
        "Return Items",
        "Back To School Supplies",
        "Furniture Shopping & Assembly",
        "Party Errands",
    ]:
        return "Run Errands"
    elif task_name in [
        "Delivery",
        "Delivery Service",
        "Drop Off Donations",
        "Pick Up & Delivery",
        "Shopping",
        "Shipping",
        "Wait for Delivery",
        "Holiday Donation Drop-off",
        "Pick-Up & Delivery",
        "Hand Out Candy",
    ]:
        return "Delivery"
    elif task_name in [
        "Moving",
        "Move Furniture Up/Downstairs",
        "Deliver Big Piece of Furniture",
        "Help Moving",
        "Heavy Lifting",
        "Help Moving / Hauling",
        "Rearrange Furniture",
        "Remove Furniture",
        "Christmas Tree Removal",
        "Remove Heavy Furniture",
        "Lifting & Shifting",
        "Packing & Unpacking",
        "Pack for a Move",
        "Office Moving",
    ]:
        return "Moving"
    elif task_name in [
        "Furniture Assembly",
        "Assemble IKEA Furniture",
        "Assemble Flat-pack",
        "Flat-pack Shopping & Assembly",
        "Disassemble furniture",
        "Holiday Assembly",
        "Toy Assembly ",
    ]:
        return "Furniture Assembly"
    elif task_name in [
        "Yard Work",
        "Garden Work & Removal",
        "Yard Work & Removal",
        "Lawn Mowing",
        "Ice Dam Removal",
        "Snow Removal",
        "Fall Yardwork",
        "Lawn Care Services",
        "Landscaping Services",
        "Winter Yardwork",
        "Sidewalk Salting",
    ]:
        return "Yard Work"
    elif task_name in [
        "Event Staffing",
        "Event Help & Wait Staff",
        "Bartending ",
        "Birthday and Party Planning",
        "Help Cooking & Serving Food",
        "Entertain Guests",
        "Event Decorating",
        "Thanksgiving Decorating",
        "Halloween Decorating",
        "Organization",
        "Decoration Help",
        "Fall Decorating",
        "Holiday Party Help",
        "Cooking & Baking",
        "Organize for Fall",
        "Event Marketing",
        "Gift Wrapping",
    ]:
        return "Event Staffing"
    elif task_name in [
        "Electrical Work",
        "Handyman",
        "General Handyman",
        "Plumbing",
        "Mounting",
        "Home Repairs",
        "Painting",
        "TV Mounting",
        "Mounting & Installation",
        "Wall Mounting",
        "Smoke Detector Maintenance",
        "Sump Pump Repair",
        "Water Heater Maintenance",
        "Carpentry",
        "Painting",
        "Winter Pool Maintenance",
        "Automotive Help",
        "Generator Installation",
        "Hang Pictures",
        "Winter Deck Maintenance",
        "Window Winterization",
        "Snowblower Maintenance",
        "Office Handyman",
        "Light Installation",
        "Pipe Insulation",
        "Home Maintenance",
        "Furnace Filter Replacement",
        "Storm Door Installation",
        "AC Winterization",
        "Personal Assistant",
        "Build New Furniture",
        "Research",
        "Office Administration",
    ]:
        return "Handyman"
    else:
        print(task_name)
        raise NotImplementedError
