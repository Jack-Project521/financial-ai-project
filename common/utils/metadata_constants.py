from langchain.chains.query_constructor.schema import AttributeInfo

# metadata_constants.py, Meta data for csv file

# Beef csv meta data
DOCUMENT_CONTENT_DESCRIPTION_BEEF = """
    This is a csv file that includes beef statistics data, 
    all columns in this csv file are shown with the following:
    {columns}
"""

METADATA_FIELD_INFO_BEEF_SMALL = [
    AttributeInfo(name="date", description="the date of the data item", type="string"),
    AttributeInfo(name="year", description="the year of the data item", type="string"),  # string
    AttributeInfo(name="week_number", description="which week in the current year, namely, week of year", type="integer"),
    AttributeInfo(name="kill_number", description="the total number of the kill", type="integer"),
    AttributeInfo(name="bone_number", description="the total number of the boning", type="string"),
    AttributeInfo(name="kill_weight", description="the total weight of the kill", type="string"),
    AttributeInfo(name="bone_weight", description="the total weight of the boning", type="string"),
    AttributeInfo(name="kill_Cost_$", description="the total cost of the kill", type="string"),
    AttributeInfo(name="bone_Cost_$", description="the total cost of the boning", type="string"),
    AttributeInfo(name="kill_cost_$/kg", description="the kill cost per kilogram", type="string"),
    AttributeInfo(name="bone_cost_$/kg", description="the boning cost per kilogram", type="string"),
    AttributeInfo(name="prod_ctn", description="the number of the cartons of production", type="string"),
    AttributeInfo(name="prod_kg", description="the total weight of the carton produced", type="string")
]

# Define the column type for the use of csv file reading
column_types = {
        "date": str,
        "year": str,  # force year into string to match AttributeInfo
        "week_number": int,
        "kill_number": int,
        "bone_number": str,
        "kill_weight": str,
        "bone_weight": str,
        "kill_Cost_$": str,
        "bone_Cost_$": str,
        "kill_cost_$/kg": str,
        "bone_cost_$/kg": str,
        "prod_ctn": str,
        "prod_kg": str
    }


METADATA_FIELD_INFO_BEEF = [
    AttributeInfo(
        name="date",
        description="the date of the data item",
        type="string",
    ),
    AttributeInfo(
        name="year",
        description="the year of the data item",
        type="string",
    ),
    AttributeInfo(
        name="week number",
        description="which week in the current year, namely, week of year",
        type="integer",
    ),
    AttributeInfo(
        name="kill number",
        description="how many cows are killed",
        type="integer",
    ),
    AttributeInfo(
        name="bone number",
        description="bone number",
        type="string",
    ),
    AttributeInfo(
        name="kill weight",
        description="kill weight",
        type="string",
    ),
    AttributeInfo(
        name="bone weight",
        description="bone weight",
        type="string",
    ),
    AttributeInfo(
        name="kill_Cost_$",
        description="kill_Cost_$",
        type="string",
    ),
    AttributeInfo(
        name="bone_Cost_$",
        description="bone_Cost_$",
        type="string",
    ),
    AttributeInfo(
        name="kill_cost_$/kg",
        description="kill_cost_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="bone_cost_$/kg",
        description="bone_cost_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="prod_ctn",
        description="prod_ctn",
        type="string",
    ),
    AttributeInfo(
        name="prod_kg",
        description="prod_kg",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARC_qty",
        description="Dsales_CARC_qty",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARC_kg",
        description="Dsales_CARC_kg",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARC_total $",
        description="Dsales_CARC_total $",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARC_$/kg",
        description="Dsales_CARC_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARC_Freight",
        description="Dsales_CARC_Freight",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARTON_qty",
        description="Dsales_CARTON_qty",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARTON_kg",
        description="Dsales_CARTON_kg",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARTON_total $",
        description="Dsales_CARTON_total $",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARTON_$/kg",
        description="Dsales_CARTON_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARTON_Freight",
        description="Dsales_CARTON_Freight",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARC_qty",
        description="Xsales_CARC_qty",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARC_kg",
        description="Xsales_CARC_kg",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARC_total $",
        description="Xsales_CARC_total $",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARC_$/kg",
        description="Xsales_CARC_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARC_Freight",
        description="Xsales_CARC_Freight",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARTON_qty",
        description="Xsales_CARTON_qty",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARTON_kg",
        description="Xsales_CARTON_kg",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARTON_total $",
        description="Xsales_CARTON_total $",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARTON_$/kg",
        description="Xsales_CARTON_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARTON_Freight",
        description="Xsales_CARTON_Freight",
        type="string",
    ),
    AttributeInfo(
        name="kill_fee_$/hd",
        description="kill_fee_$/hd",
        type="string",
    ),
    AttributeInfo(
        name="bone_fee_$/hd",
        description="bone_fee_$/hd",
        type="string",
    ),
    AttributeInfo(
        name="RP_fee_$/hd",
        description="RP_fee_$/hd",
        type="string",
    ),
    AttributeInfo(
        name="kill_fee_$/kg",
        description="kill_fee_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="bone_fee_$/kg",
        description="bone_fee_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="RP_fee_$/kg",
        description="RP_fee_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="prod_$/kg",
        description="prod_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARC_Freight_$/kg",
        description="Dsales_CARC_Freight_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Dsales_CARTON_Freight_$/kg",
        description="Dsales_CARTON_Freight_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARC_Freight_$/kg",
        description="Xsales_CARC_Freight_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_CARTON_Freight_$/kg",
        description="Xsales_CARTON_Freight_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Xsales_Intl_Freight_$/kg",
        description="Xsales_Intl_Freight_$/kg",
        type="string",
    ),
    AttributeInfo(
        name="Kill_kg/hd",
        description="Kill_kg/hd",
        type="string",
    ),
    AttributeInfo(
        name="bone_kg/hd",
        description="bone_kg/hd",
        type="string",
    ),
    AttributeInfo(
        name="kill_cost_$/hd",
        description="kill_cost_$/hd",
        type="string",
    ),
    AttributeInfo(
        name="bone_cost_$/hd",
        description="bone_cost_$/hd",
        type="string",
    ),
    AttributeInfo(
        name="Date2",
        description="Date2",
        type="string",
    )
]