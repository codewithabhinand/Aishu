from tools import Temprature_Extractor, dt, grocery_checklist

def tool_dict():
    tools = {
        "Temprature_Extractor":Temprature_Extractor.main(),
        "dt":dt.main(),
        "grocery_checklist":grocery_checklist.main()
    }
    return tools

def tool_str():
    tools = """
    Temprature_Extractor:
        This tool will provide with the weather condition provided output with the temprature.
        Example: User asks "What's the temprature?"
        Using the Temprature_Extractor get the output.
        Act: Temprature_Extractor
        Output: {"temprature":19.81}
    
    dt:
        This tools will provide us with the Current date and time.
        Example: User asks "What's the time??"
        Using the dt get the output.
        Act: dt
        Output: 2024-09-22 21:42:27.417912
        
    grocery_checklist:
        This tools will add the grocery item to the checklist.
        Example: User asks "Add item to check list"
        Using the dt get the output.
        Act: grocery_checklist
        Output: Item Added Itemname
    """
    return tools