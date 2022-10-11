import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import openpyxl
import locale
from plotly.subplots import make_subplots

FONT_AWESOME = ["//assets//fontAwesome//all.min.css"]

#app = Dash(__name__, external_stylesheets = [dbc.themes.VAPOR])
#Other cool themes
app = Dash(__name__, external_stylesheets = [dbc.themes.SUPERHERO, FONT_AWESOME])
#app = Dash(__name__, external_stylesheets = [dbc.themes.SOLAR])
#app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])
#app = Dash(__name__, external_stylesheets = [dbc.themes.QUARTZ])
server = app.server

regions_län = pd.read_excel("regions_municipalities.xlsx")
regions_län.set_index("Län", inplace = True)
cbe_emissions = pd.read_excel("CBE_emissions.xlsx")
cbe_emissions.set_index("Municipality", inplace = True)
wb = openpyxl.load_workbook("SE_data.xlsx")
cars = pd.DataFrame(wb["Ownership_cars"].values, columns=next(wb["Ownership_cars"].values)[0:])
buses = pd.DataFrame(wb["Public_buses"].values, columns=next(wb["Public_buses"].values)[0:])
pop = pd.DataFrame(wb["Population"].values, columns=next(wb["Population"].values)[0:])
dwellings_ratio = pd.DataFrame(wb["Dwellings_ratios"].values, columns=next(wb["Dwellings_ratios"].values)[0:])
dh_ef = pd.DataFrame(wb["DH-EF"].values, columns=next(wb["DH-EF"].values)[0:])
dh = pd.DataFrame(wb["DH"].values, columns=next(wb["DH"].values)[0:])
el_shares = pd.DataFrame(wb["EL-DH ratios"].values, columns=next(wb["EL-DH ratios"].values)[0:])
dwellings_ownership = pd.DataFrame(wb["Ownership_dwelling"].values, columns=next(wb["Ownership_dwelling"].values)[0:])
dwellings_tenureship = pd.DataFrame(wb["Dwellings_tenureship"].values, columns=next(wb["Dwellings_tenureship"].values)[0:])
dwellings_stock = pd.DataFrame(wb["Housing_stock"].values, columns=next(wb["Housing_stock"].values)[0:])
dwellings_size = pd.DataFrame(wb["Dwellings_total_size"].values, columns=next(wb["Dwellings_total_size"].values)[0:])
distance = pd.DataFrame(wb["Average_driven_cars"].values, columns=next(wb["Average_driven_cars"].values)[0:])
pt_cost = pd.DataFrame(wb["Public_transport_cost"].values, columns=next(wb["Public_transport_cost"].values)[0:])
pt_cost.set_index("Län", inplace=True)
regions = pd.read_excel("regions_municipalities.xlsx")
regions.set_index("Municipality",inplace =True)
offered_pt = pd.DataFrame(wb["Offered_public_transport"].values, columns=next(wb["Offered_public_transport"].values)[0:])
offered_pt.set_index("Municipality", inplace = True)
reg_pop = pd.DataFrame(wb["Region_population"].values, columns=next(wb["Region_population"].values)[0:])
reg_pop.set_index("Region", inplace=True)

dh_ef.set_index(dh_ef.columns[0], inplace=True)
dwellings_tenureship.set_index("Municipality", inplace = True)

for df in [cars, buses, pop, dwellings_ratio, dh, el_shares, dwellings_ownership, dwellings_stock,
           dwellings_size, distance]:
    df.set_index("Municipality", inplace=True)

tbe_emissions = pd.read_excel("TBE_emissions.xlsx")
tbe_emissions.set_index("Municipality", inplace=True)

app.title = "Viable Cities Finance"
app.config["suppress_callback_exceptions"] = True
percentages = list(range(0, 101))
percentages_5 = list(range(0, 101, 20))

regions_2 = ['Västra Götalands län', 'Kronobergs län', 'Dalarnas län',
       'Uppsala län', 'Norrbottens län', 'Jönköpings län',
       'Västernorrlands län', 'Skåne län', 'Västmanlands län',
       'Jämtlands län', 'Värmlands län', 'Västerbottens län',
       'Örebro län', 'Östergötlands län', 'Gävleborgs län', 'Kalmar län',
       'Stockholms län', 'Södermanlands län', 'Hallands län',
       'Gotlands län', 'Blekinge län']

municipalities = ['Ale', 'Alingsås', 'Älmhult', 'Älvdalen', 'Alvesta', 'Älvkarleby',
       'Älvsbyn', 'Åmål', 'Aneby', 'Ånge', 'Ängelholm', 'Arboga', 'Åre',
       'Årjäng', 'Arjeplog', 'Arvidsjaur', 'Arvika', 'Åsele', 'Askersund',
       'Åstorp', 'Åtvidaberg', 'Avesta', 'Båstad', 'Bengtsfors', 'Berg',
       'Bjurholm', 'Bjuv', 'Boden', 'Bollebygd', 'Bollnäs', 'Borås',
       'Borgholm', 'Borlänge', 'Botkyrka', 'Boxholm', 'Bräcke',
       'Bromölla', 'Burlöv', 'Dals-Ed', 'Danderyd', 'Degerfors',
       'Dorotea', 'Eda', 'Ekerö', 'Eksjö', 'Emmaboda', 'Enköping',
       'Eskilstuna', 'Eslöv', 'Essunga', 'Fagersta', 'Falkenberg',
       'Falköping', 'Falun', 'Färgelanda', 'Filipstad', 'Finspång',
       'Flen', 'Forshaga', 'Gagnef', 'Gällivare', 'Gävle', 'Gislaved',
       'Gnesta', 'Gnosjö', 'Göteborg', 'Götene', 'Gotland', 'Grästorp',
       'Grums', 'Gullspång', 'Habo', 'Håbo', 'Hagfors', 'Hällefors',
       'Hallsberg', 'Hallstahammar', 'Halmstad', 'Hammarö', 'Haninge',
       'Haparanda', 'Härjedalen', 'Härnösand', 'Härryda', 'Hässleholm',
       'Heby', 'Hedemora', 'Helsingborg', 'Herrljunga', 'Hjo', 'Hofors',
       'Höganäs', 'Högsby', 'Höör', 'Hörby', 'Huddinge', 'Hudiksvall',
       'Hultsfred', 'Hylte', 'Järfälla', 'Jokkmokk', 'Jönköping', 'Kalix',
       'Kalmar', 'Karlsborg', 'Karlshamn', 'Karlskoga', 'Karlskrona',
       'Karlstad', 'Katrineholm', 'Kävlinge', 'Kil', 'Kinda', 'Kiruna',
       'Klippan', 'Knivsta', 'Köping', 'Kramfors', 'Kristianstad',
       'Kristinehamn', 'Krokom', 'Kumla', 'Kungälv', 'Kungsbacka',
       'Kungsör', 'Laholm', 'Landskrona', 'Laxå', 'Lekeberg', 'Leksand',
       'Lerum', 'Lessebo', 'Lidingö', 'Lidköping', 'Lilla Edet',
       'Lindesberg', 'Linköping', 'Ljungby', 'Ljusdal', 'Ljusnarsberg',
       'Lomma', 'Ludvika', 'Luleå', 'Lund', 'Lycksele', 'Lysekil', 'Malå',
       'Malmö', 'Malung-Sälen', 'Mariestad', 'Mark', 'Markaryd',
       'Mellerud', 'Mjölby', 'Mölndal', 'Mönsterås', 'Mora', 'Mörbylånga',
       'Motala', 'Mullsjö', 'Munkedal', 'Munkfors', 'Nacka', 'Nässjö',
       'Nora', 'Norberg', 'Nordanstig', 'Nordmaling', 'Norrköping',
       'Norrtälje', 'Norsjö', 'Nybro', 'Nyköping', 'Nykvarn', 'Nynäshamn',
       'Ockelbo', 'Öckerö', 'Ödeshög', 'Olofström', 'Örebro',
       'Örkelljunga', 'Örnsköldsvik', 'Orsa', 'Orust', 'Osby',
       'Oskarshamn', 'Österåker', 'Östersund', 'Östhammar',
       'Östra Göinge', 'Ovanåker', 'Överkalix', 'Övertorneå', 'Oxelösund',
       'Pajala', 'Partille', 'Perstorp', 'Piteå', 'Ragunda', 'Rättvik',
       'Robertsfors', 'Ronneby', 'Säffle', 'Sala', 'Salem', 'Sandviken',
       'Säter', 'Sävsjö', 'Sigtuna', 'Simrishamn', 'Sjöbo', 'Skara',
       'Skellefteå', 'Skinnskatteberg', 'Skövde', 'Skurup',
       'Smedjebacken', 'Söderhamn', 'Söderköping', 'Södertälje',
       'Sollefteå', 'Sollentuna', 'Solna', 'Sölvesborg', 'Sorsele',
       'Sotenäs', 'Staffanstorp', 'Stenungsund', 'Stockholm', 'Storfors',
       'Storuman', 'Strängnäs', 'Strömstad', 'Strömsund', 'Sundbyberg',
       'Sundsvall', 'Sunne', 'Surahammar', 'Svalöv', 'Svedala',
       'Svenljunga', 'Täby', 'Tanum', 'Tibro', 'Tidaholm', 'Tierp',
       'Timrå', 'Tingsryd', 'Tjörn', 'Tomelilla', 'Töreboda', 'Torsås',
       'Torsby', 'Tranås', 'Tranemo', 'Trelleborg', 'Trollhättan',
       'Trosa', 'Tyresö', 'Uddevalla', 'Ulricehamn', 'Umeå',
       'Upplands Väsby', 'Upplands-Bro', 'Uppsala', 'Uppvidinge',
       'Vadstena', 'Vaggeryd', 'Valdemarsvik', 'Vallentuna', 'Vänersborg',
       'Vännäs', 'Vansbro', 'Vara', 'Varberg', 'Vårgårda', 'Värmdö',
       'Värnamo', 'Västerås', 'Västervik', 'Vaxholm', 'Växjö', 'Vellinge',
       'Vetlanda', 'Vilhelmina', 'Vimmerby', 'Vindeln', 'Vingåker',
       'Ydre', 'Ystad']

         
def build_banner():
    return html.Div(
        id="banner",
        className = "banner",
        children = [
            html.Div(
                id="VCF-logo-div",
                children = [
                    html.Img(id="VCF-logo",
                    src="assets/VCF_logo.png")],
            ),
            html.Div(
                id = "banner-text",
                children = [
                    html.H3("Viable Cities Finance Dashboard"),
                    html.H4("Emissions Reduction Cost Assessment - Beta"),
                    ]
                ),
            html.Div(
                id = "learn-more-button",
                children=[
                    dbc.Button("Learn More", id = "modal-opener"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("INFO BOX"),
                            dbc.ModalBody("""
                                        Want to know more about the project? Please visit us at our websites (links below) or feel free to reach us: Fedra Vanhuyse (fedra.vanhuyse@viablecities.se) and Tommaso Piseddu (tommaso.piseddu@sei.org)
                                            """),
                            dbc.ModalFooter(
                                [
                                dbc.Button("SEI Viable Cities Finance", id = "sei-button", href = "https://www.sei.org/projects-and-tools/projects/viable-cities-finance/#overview", target="_blank"),
                                dbc.Button("Viable Cities Program", id = "VC-button", href = "https://en.viablecities.se/", target="_blank"),
                                dbc.Button("Close", id = "modal-closer")]
                                )
                            ],
                        id="info-modal"),
                    dbc.Button("Glossary", id="glossary-button"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Glossary"),
                            dbc.ModalBody([
                                html.H5("Consumption-based emissions"),
                                html.P("The emissions resulting from the economic activity required to meet a nation's demand for goods and services."),
                                html.H5("Territorial emissions"),
                                html.P("Emissions that take place within a municipality's territorial boundaries and include exports but omit imports."),
                                html.H5("CAPEX"),
                                html.P("Capital Expenditure. The sum an organization, a corporate entity or a private citizen spends to buy, maintain, or improved its fixed assets (real estate assets, cars, buses, etc.)"),
                                html.H5("OPEX"),
                                html.P("Operational Expenditure. The ongoing cost for running a product, business, or system.")
                            ])
                        ],
                    id="glossary-modal"),
                    dbc.Button("Methodology", id="methodology-button"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Methodology"),
                            dbc.ModalBody([
                                html.H5("The model and the data"),
                                html.P("""To calculate the financial investments needed for climate neutral cities, we
                                developed a model consisting of a series of databases and calculations. We make use of 
                                four main databases in our model: 1) greenhouse gas emissions at the municipal level (SEI's 
                                Konsumtionskompassen project and Naturvårdsverket), 2) Population growth forecasts up to 
                                2030 (SCB), 3) Socio-economic data at city level (Trafikverket, SCB and others),
                                4) mitigation measures and costs (literature review). As the Konsumtionskompassen project
                                is still running, we report here preliminary results for emissions data at the household 
                                level. The third database is a collection of data that is relevant for our calculations,
                                such as ownership, type and size of dwellings; number and type of cars in the city;
                                composition of the public transport fleet; and information on the heating and energy sources
                                used in the city. This data allows for the allocation of the financial investment needs 
                                the stakeholders that we identified in the model: private citizens that do not own real
                                estate assets, private landlords, public transport companies, municipality housing companies,
                                utility companies, private businesses, other municipality companies.
                                In our calculations, assumptions pertain to electricity production. Wile some of the proposed
                                measures will reduce electricity consumption (e.g., energy-efficient household appliances),
                                electricity demands will spike from, for example, the electrification of vehicles. Using 
                                fossil fuels to generate the additional electricity needed will counteract the mitigation 
                                potential of electrification for the transport sector."""),
                                html.H5("The scenarios"),
                                html.P("""Three alternatives scenarios were designed to forecast emissions by 2030 at the municipal
                                level: 1) business as usual (BAU); 2) an increase in emissions; and 3) a reduction in
                                emissions. In the first option, the BAU scenario, we assumed consumption patterns and 
                                per-capita emissions profiles of 2019 will be the same in 2030. As a result of population
                                growth, even though per-capita emissions are the same, the total emissions by 2030 will 
                                increase. In our second option, we assumed an increase in emissions of 17%, building on the
                                research of Harris et al (2020). The authors forsee a 33% increase in emissions during the 
                                2007 - 2050 period, using data from nine cities in continental Europe, including Malmö. 
                                Some cities in theie research cohort might be less relevan to the Swedish settin, such as
                                Istanbul, but the increase experienced in Istanbul is at lease partially offset by Turin 
                                and Milan, where the emissions are expected to decrease in 2050 because of slower economic
                                growth compared to the othe cities in the sample. Should future emissions be significantly lower
                                than expected, the investment needed would be lower as well. In our third option, we assume
                                emissions will decrease by 6%, building on the research of Wood et al (2020). The focus 
                                of this paper is on carbon emissions by 2030, but we assume that a similar pattern could be
                                observed for the other greenhouse gases.""")
                            ])
                        ],
                    id="methodology-modal")
                    ]
                )
            ]
        )

def collapse():
  return  html.Div(
        [
#Emissions accounting methodology, municipality selection and parameters settings
        html.Div(
            id="welcome-banner",
            children=[
                html.H2("Welcome!",id="welcome-text"),
                html.P("""
                        Sweden aims to achieve net zero emissions by 2045, which equals to less than 1 tonne of greenhouse gas emissions per person (Swedish Climate Policy Framework, 2017).
                        The purpose of this dashboard is to support Swedish municipalities with their climate action and investment planning.
                        It provides 1) insight into the current emissions in the cities, from a territorial emissions perspective and a consumption-based perspective (household level data only); 2) some forecasts to 2030 using population growth and other socio-economic data; 3) a tool to see the effects of different climate actions, and their associated costs. The necessary investments are computed for different types of stakeholders, and emission profiles broken under different categories. Please note that the consumption-based emissions do not incorporate emissions from the government sector.""", id = "welcome-subtext"),
                html.Ul(id="bullet-list",
                        children=[html.Li("1. Please select a municipality", id="Li-1"), html.Li("2. Design your own climate action strategy, looking at territorial or consumption based emissions", id="Li-2"), html.Li("3. Assess the consequences of the climate action strategy mix, in terms of future emissions and costs", id="Li-3")]),
                html.Div(
                    [dcc.Dropdown(
                        id="region-dropdown",
                        options=regions_2,
                        searchable=True,
                        placeholder="Select a region")],
                    id="region-dropdown-div"),
                html.Div(
                    [dcc.Dropdown(
                        id="municipality-dropdown",
                        options=municipalities,
                        searchable=True,
                        placeholder="Select a municipality")],
                    id="municipality-dropdown-div"),
                ])
        ], id="div-1")

def collapse_2():
    return html.Div(
        [html.Div([dbc.Button(
                "Food",
                id="food-collapse",
                n_clicks=0,
                title = "The food choices we make everyday impact our carbon footprints. Vegetarian and vegan diets can significantly contribute to reduced GHG emissions."
            ),
            dbc.Collapse(
            children=[
            html.P(
                id = "slider-text-1",
                children = "Share of people that will adopt a vegan diet (2030)"
                ),
            dcc.Slider(
                id = "slider-1",
                min = min(percentages),
                max = max(percentages),
                marks = {
                    str(perc): {
                        "label": str(perc),
                        }
                    for perc in percentages_5
                },
                tooltip = {
                    "placement": "bottom",
                    "always_visible": True}
                ),
            html.P(
                id = "slider-text-2",
                children = "Share of people that will adopt a vegetarian diet (2030)"
                ),
            dcc.Slider(
                id = "slider-2",
                min = min(percentages),
                max = max(percentages),
                marks = {
                    str(perc): {
                        "label": str(perc),
                        }
                    for perc in percentages_5
                },
                tooltip = {
                    "placement": "bottom",
                    "always_visible": True}
                ),
            html.P(
                id="slider-text-3",
                children="Share of people that will reduce meat consumption (2030)"
               ),
            dcc.Slider(
                id="slider-3",
                min=min(percentages),
                max=max(percentages),
                marks={
                    str(perc): {
                        "label": str(perc),
                    }
                    for perc in percentages_5
                },
                tooltip = {
                    "placement": "bottom",
                    "always_visible": True
                }
            ),
            html.P(
                id="slider-text-4",
                children="Share of people that will adopt a nutrition diet (according to Swedish Dietary Guidelines) (2030)"
            ),
            dcc.Slider(
                id="slider-4",
                min=min(percentages),
                max=max(percentages),
                marks={
                    str(perc): {
                        "label": str(perc),
                    }
                    for perc in percentages_5
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            ),
            html.P(
                id="slider-text-5",
                children="Share of people that will not change its diet (2030)"
            ),
            dcc.Slider(
                id="slider-5",
                min=min(percentages),
                max=max(percentages),
                marks={
                    str(perc): {
                        "label": str(perc),
                    }
                    for perc in percentages_5
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            ),
        ],
        id = "collapse-1",
        is_open = False),
        html.Div(
        [dbc.Button(
            "Clothing",
            id="clothing-collapse-button",
            n_clicks=0,
            title = "Fast fashion has led to a big increase in the quantity of clothers produced and thrown away. Clothes, footwear and hosehold textiles are responsible for water pollution, GHG emissions and landfill"),
        dbc.Collapse(
            id="clothing-collapse",
            children=[
                html.P(
                    id="slider-text-6",
                    children="Share of people that will reduce clothing consumption by 30% (2030)"
                ),
                dcc.Slider(
                    id="slider-6",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc),
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                ),
                html.P(
                    id="slider-text-7",
                    children="Share of people doubling the life of their garments"
                ),
                dcc.Slider(
                    id="slider-7",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                )
            ],
            is_open=False
        )
        ]),
        html.Div(
            [dbc.Button(
                "Housing",
                id="housing-collapse-button",
                n_clicks=0,
                title="Furniture consumption contributes to global warming due to its production processes and by reducing carbon uptake from forests"
            ),
            dbc.Collapse(
                id="housing-collapse",
                children=[
                    html.P(
                        id="slider-text-8",
                        children="Share of people that halves furniture consumption"
                    ),
                    dcc.Slider(
                        id="slider-8",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                ],
                is_open=False
            )]
        ),
        html.Div(
            [dbc.Button(
                "Transport services",
                id="transport-collapse-button",
                n_clicks=0,
                title="Transport services, whether of people or of goods, represent one of the main drivers of GHG emissions"
            ),
            dbc.Collapse(
                id="transport-collapse",
                children=[
                    html.P(
                        id="slider-text-9",
                        children="Share of electric public buses"
                    ),
                    dcc.Slider(
                       id="slider-9",
                       min=min(percentages),
                       max=max(percentages),
                       marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                       tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                    html.P(
                        id="slider-text-10",
                        children="Share of public buses that runs on conventional HVO"
                    ),
                    dcc.Slider(
                        id="slider-10",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                    html.P(
                        id="slider-text-11",
                        children="Share of buses that will continue to run on the current fuel mix"
                    ),
                    dcc.Slider(
                        id="slider-11",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                    html.P(
                        id="slider-text-12",
                        children="Share of buses that will run on hybrid HVO"
                    ),
                    dcc.Slider(
                        id="slider-12",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                ]
                )
                ]
            ),
            html.Div(
                [dbc.Button(
                    "Air transport",
                    id="air-collapse-button",
                    n_clicks=0,
                    title="According to data, aviation is responsible for about 2.5% of global CO2 emissions, but its actual impact on climate change is much higher."),
                dbc.Collapse(
                    id="air-collapse",
                    children=[
                        html.P(
                            id="slider-text-13",
                            children="Reduction in air transport"
                        ),
                    dcc.Slider(
                        id="slider-13",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                    ]
                )]
            ),
            html.Div(
                [dbc.Button(
                    "Recreation",
                id="recreation-collapse-button",
                n_clicks=0,
                title="Recreational activities contribute, even if marginally, to GHG emissions. From a consumption-based emissions perspective, this is even more true when considering the emissions that are linked to production of the necessary equipment"),
                dbc.Collapse(
                    id="recreation-collapse",
                    children=[
                        html.P(
                            id="slider-text-14",
                            children="Share of people doubling the life of their recreation equipment"
                        ),
                    dcc.Slider(
                    id="slider-14",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                ),
                    html.P(
                        id="slider-text-15",
                        children="Share of people quitting using package holidays"
                    ),
                    dcc.Slider(
                        id="slider-15",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                    ]
                )]
            ),
            html.Div(
                [dbc.Button(
                    "Restaurants and hotels",
                    id="rh-collapse-button",
                    n_clicks=0,
                    title="Restaurants and hotels contribute to GHG emissions. In this sense, we mainly consider the emissions that can be saved by reducing food waste"
                ),
                dbc.Collapse(
                    id="rh-collapse",
                    children=[
                        html.P(
                            id="slider-text-16",
                            children="Share of catering service providers that is able to reach the potential reduction in waste that as identified by Erikkson et al. (2017)"
                        ),
                        dcc.Slider(
                            id="slider-16",
                            min=min(percentages),
                            max=max(percentages),
                            marks={
                                str(perc): {
                                    "label": str(perc)
                                }
                                for perc in percentages_5
                            },
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True
                            }
                        )
                    ]
                )]
            ),
            html.Div(
                [dbc.Button(
                    "Vehicles",
                    id="vehicles-collapse-button",
                    n_clicks=0,
                    title = "Vehicles manufacturing and fuel use in private vehicles is the main sector of golobal GHG emissions"
                ),
                dbc.Collapse(
                    id="vehicles-collapse",
                    children=[
                        html.P(
                            id="slider-text-17",
                            children="Share of private cars that will be electrified"
                        ),
                    dcc.Slider(
                        id="slider-17",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                        html.P(
                            id="slider-text-18",
                            children="Share of private cars that will be given up in favour of public transport"
                        ),
                    dcc.Slider(
                        id="slider-18",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                        html.P(
                            id="slider-text-19",
                            children="Share of private cars that will still run on the current average fleet's fuel"
                        ),
                    dcc.Slider(
                        id="slider-19",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                        html.P(
                            id="slider-text-20",
                            children="Share of plug-in-hybrid private cars"
                        ),
                    dcc.Slider(
                        id="slider-20",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                        html.P(
                            id="slider-text-21",
                            children="Share of private cars that will run on hydrogen"
                        ),
                    dcc.Slider(
                        id="slider-21",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                    ]
                )]
            ),
            html.Div(
                [dbc.Button(
                    "Electricity",
                    id="electricity-collapse-button",
                    n_clicks=0,
                    title="The use of more energy-saving home appliances can contribute to a reduction of households' carbon footprint"
                ),
                dbc.Collapse(
                    id="electricity-collapse",
                    children=[
                        html.P(
                            id="slider-text-22",
                            children="Share of households that will be equipped with BAT major appliances"
                        ),
                    dcc.Slider(
                        id="slider-22",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible":  True
                        }
                    )
                    ]
                )]
            ),
            html.Div(
                [dbc.Button(
                    "District heating",
                    id="dh-collapse-button",
                    n_clicks=0,
                    title = "Reducing the share of heat that is produced using fossil fuels is the most effective way to guarantee a clear district heat supply"
                ),
                dbc.Collapse(
                    id="dh-collapse",
                    children=[
                        html.P(
                            id="slider-text-23",
                            children="Share of fossil fuel DH production that is shifted to wood pellets"
                        ),
                    dcc.Slider(
                        id="slider-23",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                    ]
                )]
            ),
            html.Div(
                [dbc.Button(
                    "House heating",
                    id="hh-collapse-button",
                    n_clicks=0,
                    title = "Better retrofitting and reduction of indoor temperature contribute to a lower heat demand and allow for this to be met only through sustainable fuels"
                ),
                dbc.Collapse(
                    id="hh-collapse",
                    children=[
                        html.P(
                            id="slider-text-24",
                            children="Share of households where indoor temperature is reduce to 20°C"
                        ),
                    dcc.Slider(
                        id="slider-24",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                        html.P(
                            id="slider-text-25",
                            children="Share of households where no heating measure is implemented"
                        ),
                    dcc.Slider(
                        id="slider-25",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                        html.P(
                            id="slider-text-26",
                            children="Share of households where the measures in Savvidou and Nykvist (2020) are implemented"
                        ),
                    dcc.Slider(
                        id="slider-26",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                    ]
                )]
            )], id="sliders-div"),
            html.Div(
                children=[
                    html.Div([
                    html.Div([html.H2("Emissions", id="graph-title")], id = "graph-title-div"),
                    html.Div([
                        html.P(
                            "Please select a scenario:"
                        ),
                        dcc.Dropdown(
                            id="scenario-dropdown-list",
                            options=["BAU Scenario", "Scenario 2", "Scenario 3"],
                            value="BAU Scenario",
                            searchable=True,
                            placeholder="..."
                        )],
                        id="scenario-dropdown")],
                    id="over-the-graph-div"),
                    html.Hr(),
            html.Div(
                id="graph-space",
                children=[
                    dcc.Graph(id="results-graph",
                              config={'displaylogo': False}
                              )]
            )], id="sidebar"),
            html.Hr(id="graphs-separator"),
            html.Div([html.H1("Investments")], id="investments-title-div"),
            html.Div([
                html.P(
                    "Please select an actor:"
                ),
                dcc.Dropdown(
                    id="actors-dropdown-list",
                    options=["Privates - tenants", "Privates - landlords and homeowners", "Public transport company", "Municipality housing company",
                             "Utility company", "Private businesses", "Municipality", "Total"],
                    searchable=True,
                    placeholder="..."
                )
            ],id="actors-dropdown"),
            html.Div(
                id="cost-CBE-graph-div",
                children=[
                    dcc.Graph(id="cost-CBE-graph", config={'displaylogo': False})]
            ),
        html.Div(
            id = "opex-CBE-graph-div",
            children =[html.Hr(id="graphs-separator-1"),
            dcc.Graph(id="opex-CBE-graph", config={'displaylogo': False})]
        ),
        html.Div(
            id="funders-space",
            children = [
                html.Img(
                    id="funders-img",
                    src="assets/funders-logo.png")
            ]
        )],
        id="div-2"
            )


def collapse_3():
    return html.Div(
            children=[
                html.Div([dbc.Button(
                    "Transport service",
                    id="transport-service-collapse-button",
                    n_clicks=0
                ),
                dbc.Collapse(
                    id= "transport-service-collapse",
                    is_open=False,
                children = [html.P(
                id="slider-text-27",
                children="Share of buses that is electrified"
            ),
            dcc.Slider(
                id="slider-27",
                min=min(percentages),
                max=max(percentages),
                marks={
                    str(perc): {
                        "label": str(perc)
                    }
                    for perc in percentages_5
                    },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            ),
            html.P(
                id="slider-text-28",
                children="Share of buses that run on conventional HVO"
            ),
            dcc.Slider(
                id="slider-28",
                min=min(percentages),
                max=max(percentages),
                marks={
                    str(perc): {
                        "label": str(perc)
                    }
                    for perc in percentages_5
                    },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            ),
            html.P(
                id="slider-text-29",
                children="Share of buses that will continue running on the current fuel mix"
            ),
            dcc.Slider(
                id="slider-29",
                min=min(percentages),
                max=max(percentages),
                marks={
                    str(perc): {
                        "label": str(perc)
                    }
                    for perc in percentages_5
                    },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            ),
            html.P(
                id="slider-text-30",
                children="Share of hybrid HVO buses"
            ),
            dcc.Slider(
                id="slider-30",
                min=min(percentages),
                max=max(percentages),
                marks={
                    str(perc): {
                        "label": str(perc)
                    }
                    for perc in percentages_5
                    },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            )]),
            html.Div(
                children=
                [dbc.Button(
                    "Air transport",
                    id="air-transport-collapse-button",
                    n_clicks=0
                ),
                 dbc.Collapse(
                     id="air-transport-collapse",
                     is_open=False,
                     children=[
                html.P(
                    id="slider-text-31",
                    children="Reduction in air transport"
                ),
                dcc.Slider(
                    id="slider-31",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                        },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                )]
            )]),
            html.Div(
                children=
                [dbc.Button(
                    "Vehicles",
                    id="vehicles-cars-collapse-button",
                    n_clicks=0
                ),
                    dbc.Collapse(
                        id="vehicles-cars-collapse",
                        is_open=False,
                        children=[
                html.P(
                    id="slider-text-32",
                    children="Share of cars that will be electrified"
                ),
                dcc.Slider(
                    id="slider-32",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                ),
                html.P(
                    id="slider-text-33",
                    children="Share of cars that will be given up in favor of public transport"
                ),
                dcc.Slider(
                    id="slider-33",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                ),
                html.P(
                    id="slider-text-34",
                    children="Share of cars that will run on the current fuel mix"
                ),
                dcc.Slider(
                    id="slider-34",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                ),
                html.P(
                    id="slider-text-35",
                    children="Share of plug-in-hybrid cars"
                ),
                dcc.Slider(
                    id="slider-35",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                ),
                html.P(
                    id="slider-text-41",
                    children="Share of hydrogen cars"
                ),
                dcc.Slider(
                    id="slider-41",
                    min=min(percentages),
                    max=max(percentages),
                    marks={
                        str(perc): {
                            "label": str(perc)
                        }
                        for perc in percentages_5
                    },
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True
                    }
                )
                ])]
            ),
            html.Div(
                children=[
                    dbc.Button(
                        "Electricity",
                        id="el-collapse-button",
                        n_clicks=0
                    ),
                    dbc.Collapse(
                        id="el-collapse",
                        is_open=False,
                        children=[
                    html.P(
                        id="slider-text-36",
                        children="Share of households where BAT major appliances are purchased"
                    ),
                    dcc.Slider(
                        id="slider-36",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                ])]
            ),
            html.Div(
                children=[
                    dbc.Button(
                        "House heating",
                        id="house-heating-collapse-button"
                    ),
                    dbc.Collapse(
                        id="house-heating-collapse",
                        is_open=False,
                        children=[
                    html.P(
                        id="slider-text-37",
                        children="Share of households where indoor temperature is reduced to 20°C"
                    ),
                    dcc.Slider(
                        id="slider-37",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                    html.P(
                        id="slider-text-38",
                        children="Share of households where no heating measure is implemented"
                    ),
                    dcc.Slider(
                        id="slider-38",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    ),
                    html.P(
                        id="slider-text-39",
                        children="Share of households where the measures in Savvidou and Nykvist (2020) are implemented"
                    ),
                    dcc.Slider(
                        id="slider-39",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                ])]
            ),
            html.Div(
                children=[
                    dbc.Button(
                        "Heavy trucks",
                        id="heavy-collapse-button",
                    ),
                    dbc.Collapse(
                        id="heavy-collapse",
                        is_open=False,
                        children=[
                    html.P(
                        id="slider-text-40",
                        children="Share of diesel heavy trucks that is replaced by LBG heavy trucks"
                    ),
                    dcc.Slider(
                        id="slider-40",
                        min=min(percentages),
                        max=max(percentages),
                        marks={
                            str(perc): {
                                "label": str(perc)
                            }
                            for perc in percentages_5
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True
                        }
                    )
                ])]
            )], id="sliders-div-2"),
                html.Div(
                    children=[
                        html.Div([
                            html.Div([html.H2("Emissions", id="graph-title-2")], id="graph-title-2-div"),
                            html.Div([html.P(
                                "Please select a scenario:"
                            ),
                            dcc.Dropdown(
                                id="scenario-dropdown-list-2",
                                options=["BAU Scenario", "Scenario 2", "Scenario 3"],
                                value="BAU Scenario",
                                searchable=True,
                                placeholder="..."
                            )],id="scenario-dropdown-div-2"),
                            html.Hr(),
                            html.Div(
                                id="graph-space-2",
                                children=[
                                    dcc.Graph(id="results-graph-2", config={'displaylogo': False}
                                              )]),
                        ],
                            id="scenario-dropdown-2")],
                    id="sidebar-2"),
                html.Div(
                    children=[
                        html.Hr(id="graphs-separator-2"),
                        html.P(
                            "Please select an actor:",
                            id="actor-selection-sentence"
                        ),
                        dcc.Dropdown(
                            id="actors-dropdown-list-2",
                            options=["Privates - tenants", "Privates - landlords and homeowners", "Public transport company", "Municipality housing company",
                            "Private businesses", "Municipality", "Total"],
                            searchable=True,
                            placeholder="..."
                        )
                    ],
                    id="actors-dropdown-2"
                ),
                html.Div(
                    id="CAPEX-TBE-graph-space",
                    children=[
                        dcc.Graph(id="CAPEX-TBE-graph", config={'displaylogo': False})
                    ]
                ),
                html.Hr(id="graphs-separator-3"),
                html.Div(
                    id="OPEX-TBE-graph-space",
                    children=[
                        dcc.Graph(id="OPEX-TBE-graph", config={'displaylogo': False})
                    ]
                ),
                html.Div(
                    id="funders-space-2",
                    children=[
                        html.Img(
                            id="funders-img-2",
                            src="assets/funders-logo.png")
                    ]
                )
            ], id ="big-div-TBE")

@app.callback(
    [Output("results-graph", "figure"), Output("slider-5", "value"), Output("slider-11", "value"), Output("slider-19", "value"),
     Output("slider-25", "value")],
    [Input("municipality-dropdown", "value"), Input("slider-1", "value"), Input("slider-2", "value"),
     Input("slider-3", "value"), Input("slider-4", "value"), Input("slider-5", "value"), Input("slider-6", "value"),
     Input("slider-7", "value"), Input("slider-8", "value"), Input("slider-13", "value"), Input("slider-14", "value"),
     Input("slider-15", "value"), Input("slider-16", "value"), Input("slider-18", "value"), Input("slider-9", "value"),
     Input("slider-10", "value"), Input("slider-11", "value"), Input("slider-12", "value"), Input("slider-17", "value"),
     Input("slider-19", "value"), Input("slider-20", "value"), Input("slider-21", "value"), Input("slider-22", "value"),
     Input("slider-25", "value"), Input("slider-24", "value"), Input("slider-26", "value"), Input("slider-23", "value"),
     Input("scenario-dropdown-list", "value")]
)
def render_page_2(mun, vegan, veg, meat, nutrition, diet, reduction_clothes, doubling_clothes, half_furn, red_air,
                  double_life, package_holidays, rh_share, cars_givenup, share_elbus, share_HVObus, share_currentmixbus,
                  share_hibHVObus, share_elcars, share_currentmixcar, share_plugincar, share_hydrcar, BATel, dwell_unchanged,
                  dwell_20C, dwell_SN, dh_red, scenario):

    if mun is None:
        fig = go.Figure()
        fig.add_annotation(
            x = 2.7,
            y = 1.8,
            text = "Please make sure to select a municipality from above.",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return[go.Figure(data=fig), diet, share_currentmixbus, share_currentmixcar, dwell_unchanged]

    if dh_red is None:
        dh_red = 0
    if dwell_unchanged is None:
        dwell_unchanged = 0
    if dwell_20C is None:
        dwell_20C = 0
    if dwell_SN is None:
        dwell_SN = 0
    if share_hydrcar is None:
        share_hydrcar = 0
    if share_plugincar is None:
        share_plugincar = 0
    if share_currentmixcar is None:
        share_currentmixcar = 0
    if share_elcars is None:
        share_elcars = 0
    if reduction_clothes is None:
        reduction_clothes = 0
    if doubling_clothes is None:
        doubling_clothes = 0
    if half_furn is None:
        half_furn = 0
    if red_air is None:
        red_air = 0
    if double_life is None:
        double_life = 0
    if package_holidays is None:
        package_holidays = 0
    if rh_share is None:
        rh_share = 0
    if cars_givenup is None:
        cars_givenup = 0
    if nutrition is None:
        nutrition = 0
    if diet is None:
        diet = 0
    if meat is None:
        meat = 0
    if veg is None:
        veg = 0
    if vegan is None:
        vegan = 0
    if share_elbus is None:
        share_elbus = 0
    if share_currentmixbus is None:
        share_currentmixbus = 0
    if share_HVObus is None:
        share_HVObus = 0
    if share_hibHVObus is None:
        share_hibHVObus = 0
    if BATel is None:
        BATel = 0

    share_currentmixbus = 100 - share_elbus - share_HVObus - share_hibHVObus
    diet = 100 - vegan - veg - meat - nutrition
    share_currentmixcar = 100 - share_elcars - share_plugincar - share_hydrcar - cars_givenup
    dwell_unchanged = 100-max([dwell_SN, dwell_20C])

# Emissions computations
    food = cbe_emissions.loc[str(mun), "bread and cereals":"low alcoholic beer"].sum() * (0.33 * (vegan / 100) + 0.66 * (veg / 100) + 0.75 * (meat / 100) + 0.75 * (nutrition / 100) + (diet / 100)) + cbe_emissions.loc[str(mun), "tobacco":"narcotics"].sum()
    clothing = cbe_emissions.loc[str(mun), "clothing material":"repair and hire of footwear"].sum() * (0.7 * reduction_clothes + 0.5 * doubling_clothes + (100 - reduction_clothes - doubling_clothes))/100
    housing = cbe_emissions.loc[str(mun), "actual rentals paid by tenants, exclusive of heating":"materials and services for the maintenance and repair of the dwelling"].sum() + cbe_emissions.loc[str(mun), "gas":"solid fuels, coal, coke, briquettes, firewood, charcoal, peat and the like"].sum() + cbe_emissions.loc[str(mun), "major household appliances whether electric or not":"domestic services and household services"].sum() + cbe_emissions.loc[str(mun), "furniture and furnishings":"household textiles"].sum() * (1 - 0.5 * (half_furn/100))
    health = cbe_emissions.loc[str(mun), "pharmaceutical products":"hospital services incl. medical fee"].sum()
    air_transport = cbe_emissions.loc[str(mun), "passenger transport by air"] * (100 - red_air)/100
    recreation = ((100 - package_holidays)/100) * cbe_emissions.loc[str(mun), "package holidays"] + ((100 - double_life)/100) * cbe_emissions.loc[str(mun), ["major durables for outdoor recreation", "equipment for sport, camping and open-air recreation"]].sum() + ((100 - (double_life/100)*50)/100) * cbe_emissions.loc[str(mun), ["major durables for outdoor recreation", "equipment for sport, camping and open-air recreation"]].sum() + cbe_emissions.loc[str(mun), "equipment for the reception, recording and reproduction of sound and pictures":"repair of audio-visual, photographic and information processing equipment"].sum() + cbe_emissions.loc[str(mun), "musical instruments and major durables for indoor recreation":"games, toys and hobbies"].sum() + cbe_emissions.loc[str(mun), "plants and flowers, Christmas trees, specially treated soils, pots and pot holders.":"stationery and drawing materials"].sum()
    rh = cbe_emissions.loc[str(mun), "catering services"] * ((100 - rh_share * 0.33)/100) + cbe_emissions.loc[str(mun), "accommodation services"]

# The computation for public transport is a bit more complicated
    pop_growth = pop.loc[str(mun), 2030]/pop.loc[str(mun), 2019]
    pop_car_ratio = pop.loc[str(mun), 2019]/cars.loc[str(mun), "Number of cars"]
    cars_2030 = pop_growth * cars.loc[str(mun), "Number of cars"]
    bus_capacity = 130
    buses_2030 = pop_growth * buses.loc[str(mun), "Total"]
    total_buses_2030 = buses_2030 + ((cars_givenup/100) * cars_2030 * pop_car_ratio) / bus_capacity
    bus_increase = total_buses_2030/buses_2030
    share_diesel_bus = buses.loc[str(mun), "Diesel"]/buses.loc[str(mun), "Total"]

    pt = cbe_emissions.loc[str(mun), "tax benefit cars and hire of personal transport equipment without drivers":"passenger transport by railway"].sum() + cbe_emissions.loc[str(mun), "passenger transport by sea and inland waterway":"other purchased transport services, removal and storage services"].sum() + (share_diesel_bus/100) * (share_elbus * 0.17 + share_HVObus * 0.37 + share_hibHVObus * 0.28 + share_currentmixbus) * bus_increase * cbe_emissions.loc[str(mun), "passenger transport by road"]

# The computation for vehicles emissions is complicated as well

    share_diesel_cars = cars.loc[str(mun), "Cars-diesel"]/cars.loc[str(mun), "Number of cars"]
    share_petrol_cars = cars.loc[str(mun), "Cars-petrol"]/cars.loc[str(mun), "Number of cars"]

    vehicles = cbe_emissions.loc[str(mun), "driving lessons, driving tests and driving licences":"parking"].sum() + cbe_emissions.loc[str(mun), "motor cycles":"bicycles"].sum() + ((share_elcars/100) * (0.35 * share_diesel_cars + 0.25 * share_petrol_cars) + (share_hydrcar/100) * (0.55 * share_diesel_cars + 0.42 * share_petrol_cars) + (share_hydrcar/100) * (0.89 * share_diesel_cars + 0.67 * share_petrol_cars) + (share_currentmixcar/100)) * (cbe_emissions.loc[str(mun), "motor cars"] + cbe_emissions.loc[str(mun), "spare parts and accessories for personal transport equipment":"maintenance and repair of personal transport equipment"].sum() + cbe_emissions.loc[str(mun), "Household fuel use in private vehicles"])

    others = cbe_emissions.loc[str(mun), "hairdressing salons and personal grooming establishments":"fees for legal services, employment agencies, etc."].sum()
    el = cbe_emissions.loc[str(mun), "electricity"] * ((100 - BATel * 0.2075)/100)
    heat = ((dwellings_ratio.loc[str(mun), "1,2 Dwellings"] * (dwell_unchanged + dwell_20C * (1 - 0.21) + dwell_SN * (1 - 0.26))/100) + (dwellings_ratio.loc[str(mun), "Multiple dwellings"] * (dwell_unchanged + dwell_20C * (1 - 0.27) + dwell_SN * (1 - 0.27))/100)) * cbe_emissions.loc[str(mun), "Household fuel use in the home"]
    dist_heating = ((1 - dh_red/100) * cbe_emissions.loc[str(mun), "heat energy purchased from district heating plants."] + (dh_red/100) * (dh.loc[str(mun), "Stenkol (GWh)":"Övrigt fossilt bränsle (GWh)"].sum() + dh.loc[str(mun), "Flue gas condensation energy of fossil origin (GWh)"]) * np.mean([dh_ef.loc["Total (g CO2ekv/kWh)", "Primära trädbränslen"], dh_ef.loc["Total (g CO2ekv/kWh)", "Sekundära trädbränslen"], dh_ef.loc["Total (g CO2ekv/kWh)", "Pellets, briketter och pulver"]]) * cbe_emissions.loc[str(mun), "heat energy purchased from district heating plants."]/np.mean(dh_ef.loc["Total (g CO2ekv/kWh)", "Stenkol":"Övrigt fossilt"])) * ((dwellings_ratio.loc[str(mun), "1,2 Dwellings"] * (dwell_unchanged + dwell_20C * (1 - 0.21) + dwell_SN * (1 - 0.26))/100) + (dwellings_ratio.loc[str(mun), "Multiple dwellings"] * (dwell_unchanged + dwell_20C * (1 - 0.27) + dwell_SN * (1 - 0.27))/100))

    total = food + clothing + housing + health + air_transport + recreation + rh + pt + vehicles + el + heat + dist_heating + others

    plot_data = pd.DataFrame([-food, -clothing, -housing, -health, -air_transport, -recreation, -rh, -pt, -vehicles, -el, -heat,
           -dist_heating, -others, -food*1.1683, -clothing*1.1683, -housing*1.1683, -health*1.1683, -air_transport*1.1683,
            -recreation*1.1683, -rh*1.1683, -pt*1.1683, -vehicles*1.1683, -el*1.1683, -heat*1.1683, -dist_heating*1.1683, -others*1.1683,
            -food*0.94, -clothing*0.94, -housing*0.94, -health*0.94, -air_transport*0.94, -recreation*0.94, -rh*0.94, -pt*0.94,
            -vehicles*0.94, -el*0.94, -heat*0.94, -dist_heating*0.94, -others*0.94], columns = ["Var"])
    plot_data["Scenario"] = ["BAU Scenario"] * 13 + ["Scenario 2"] * 13 + ["Scenario 3"] * 13

# I construct the benchmark values
    food_2019 = cbe_emissions.loc[str(mun), "bread and cereals":"low alcoholic beer"].sum() + cbe_emissions.loc[str(mun), "tobacco":"narcotics"].sum()
    clothing_2019 = cbe_emissions.loc[str(mun), "clothing material":"repair and hire of footwear"].sum()
    housing_2019 = cbe_emissions.loc[str(mun), "actual rentals paid by tenants, exclusive of heating":"materials and services for the maintenance and repair of the dwelling"].sum() + cbe_emissions.loc[str(mun), "gas":"solid fuels, coal, coke, briquettes, firewood, charcoal, peat and the like"].sum() + cbe_emissions.loc[str(mun), "major household appliances whether electric or not":"domestic services and household services"].sum() + cbe_emissions.loc[str(mun), "furniture and furnishings":"household textiles"].sum()
    health_2019 = cbe_emissions.loc[str(mun), "pharmaceutical products":"hospital services incl. medical fee"].sum()
    air_transport_2019 = cbe_emissions.loc[str(mun), "passenger transport by air"]
    recreation_2019 = cbe_emissions.loc[str(mun), "package holidays"] + cbe_emissions.loc[str(mun), ["major durables for outdoor recreation", "equipment for sport, camping and open-air recreation"]].sum() + cbe_emissions.loc[str(mun), ["major durables for outdoor recreation", "equipment for sport, camping and open-air recreation"]].sum() + cbe_emissions.loc[str(mun), "equipment for the reception, recording and reproduction of sound and pictures":"repair of audio-visual, photographic and information processing equipment"].sum() + cbe_emissions.loc[str(mun), "musical instruments and major durables for indoor recreation":"games, toys and hobbies"].sum() + cbe_emissions.loc[str(mun), "plants and flowers, Christmas trees, specially treated soils, pots and pot holders.":"stationery and drawing materials"].sum()
    rh_2019 = cbe_emissions.loc[str(mun), "catering services"] + cbe_emissions.loc[str(mun), "accommodation services"]
    pt_2019 = cbe_emissions.loc[str(mun), "tax benefit cars and hire of personal transport equipment without drivers":"passenger transport by railway"].sum() + cbe_emissions.loc[str(mun), "passenger transport by sea and inland waterway":"other purchased transport services, removal and storage services"].sum() +  cbe_emissions.loc[str(mun), "passenger transport by road"]
    vehicles_2019 = cbe_emissions.loc[str(mun), "driving lessons, driving tests and driving licences":"parking"].sum() + cbe_emissions.loc[str(mun), "motor cycles":"bicycles"].sum() + (cbe_emissions.loc[str(mun), "motor cars"] + cbe_emissions.loc[str(mun), "spare parts and accessories for personal transport equipment":"maintenance and repair of personal transport equipment"].sum() + cbe_emissions.loc[str(mun), "Household fuel use in private vehicles"])
    others_2019 = cbe_emissions.loc[str(mun), "hairdressing salons and personal grooming establishments":"fees for legal services, employment agencies, etc."].sum()
    el_2019 = cbe_emissions.loc[str(mun), "electricity"]
    heat_2019 = cbe_emissions.loc[str(mun), "Household fuel use in the home"]
    dist_heating_2019 = cbe_emissions.loc[str(mun), "heat energy purchased from district heating plants."]

    total_2019 = food_2019 + clothing_2019 + housing_2019 + health_2019 + air_transport_2019 + recreation_2019 + rh_2019 + pt_2019 + vehicles_2019 + others_2019 + el_2019 + heat_2019 + dist_heating_2019

    if scenario == "BAU Scenario":
        hrz = ["Food", "Clothing", "Housing", "Health", "Air transport", "Recreation",
               "Restaurants and hotels", "Public transport", "Vehicles", "Electricity", "Heating", "District heating",
               "Others"]
        fig = make_subplots(1,2, subplot_titles=["2019: {} Kg".format(round(total_2019,2)), "2030: {} Kg".format(round(total, 2))],
                            specs=[[{"type": "pie"}, {"type": "pie"}]])
        fig.add_trace(go.Pie(labels=hrz, values = [food_2019, clothing_2019, housing_2019, health_2019, air_transport_2019,
                    recreation_2019, rh_2019, pt_2019, vehicles_2019, el_2019, heat_2019, dist_heating_2019, others_2019],
                    texttemplate = "%{value:.1f}", name = "Emissions profile by 2019 in {} (Kg of CO2-eq)".format(mun)), 1, 1)
        fig.add_trace(go.Pie(labels=hrz, values = [food, clothing, housing, health, air_transport, recreation, rh, pt, vehicles, el, heat,
           dist_heating, others], texttemplate = "%{value:.1f}", name = "Emissions profile by 2030 in {} (Kg of CO2-eq)".format(mun)), 1, 2)
        fig.update_layout(title_text='Emissions profile in {} (per-capita KG of CO2-eq)'.format(mun))
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                          marker=dict(line=dict(color='#000000', width=1)))

        return [fig, diet, share_currentmixbus, share_currentmixcar, dwell_unchanged]

    elif scenario == "Scenario 2":

        hrz = ["Food", "Clothing", "Housing", "Health", "Air transport", "Recreation",
               "Restaurants and hotels", "Public transport", "Vehicles", "Electricity", "Heating", "District heating",
               "Others"]
        total = food*1.1683 + clothing*1.1683 + housing*1.1683 + health*1.1683 + air_transport*1.1683 + recreation*1.1683 + rh*1.1683 + pt*1.1683 + vehicles*1.1683 + el*1.1683 + heat*1.1683 + dist_heating*1.1683 + others*1.1683

        fig = make_subplots(1, 2, subplot_titles=["2019: {} Kg".format(round(total_2019,2)), "2030: {} Kg".format(round(total, 2))],
                            specs=[[{"type": "pie"}, {"type": "pie"}]])
        fig.add_trace(
            go.Pie(labels=hrz, values=[food_2019, clothing_2019, housing_2019, health_2019, air_transport_2019,
                                       recreation_2019, rh_2019, pt_2019, vehicles_2019, el_2019, heat_2019,
                                       dist_heating_2019, others_2019],
                   texttemplate="%{value:.1f}", name="Emissions profile by 2019 in {} (Kg of CO2-eq)".format(mun)), 1,
            1)
        fig.add_trace(go.Pie(labels=hrz,
                             values=[food*1.1683, clothing*1.1683, housing*1.1683, health*1.1683, air_transport*1.1683, recreation*1.1683, rh*1.1683, pt*1.1683, vehicles*1.1683, el*1.1683,
                                     heat*1.1683, dist_heating*1.1683, others*1.1683], texttemplate="%{value:.1f}",
                             name="Emissions profile by 2030 in {} (Kg of CO2-eq)".format(mun)), 1, 2)
        fig.update_layout(title_text='Emissions profile in {} (per-capita KG of CO2-eq)'.format(mun))
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                          marker=dict(line=dict(color='#000000', width=1)))

        return [fig, diet, share_currentmixbus, share_currentmixcar, dwell_unchanged]

    elif scenario == "Scenario 3":
        my_data = plot_data["Var"][plot_data["Scenario"] == "BAU Scenario"]

        hrz = ["Food", "Clothing", "Housing", "Health", "Air transport", "Recreation",
               "Restaurants and hotels", "Public transport", "Vehicles", "Electricity", "Heating", "District heating",
               "Others"]
        vrt = list(my_data)
        total = food*0.94 + clothing*0.94 + housing*0.94 + health*0.94 + air_transport*0.94 + recreation*0.94 + rh*0.94 + pt*0.94 + vehicles*0.94 + el*0.94 + heat*0.94 + dist_heating*0.94 + others*0.94

        fig = make_subplots(1, 2, subplot_titles=["2019: {} Kg".format(round(total_2019,2)), "2030: {} Kg".format(round(total))],
                            specs=[[{"type": "pie"}, {"type": "pie"}]])
        fig.add_trace(
            go.Pie(labels=hrz, values=[food_2019, clothing_2019, housing_2019, health_2019, air_transport_2019,
                                       recreation_2019, rh_2019, pt_2019, vehicles_2019, el_2019, heat_2019,
                                       dist_heating_2019, others_2019],
                   texttemplate="%{value:.1f}", name="Emissions profile by 2019 in {} (Kg of CO2-eq)".format(mun)), 1,
            1)
        fig.add_trace(go.Pie(labels=hrz,
                             values=[food*0.94, clothing*0.94, housing*0.94, health*0.94,
                                     air_transport*0.94, recreation*0.94, rh*0.94, pt*0.94,
                                     vehicles*0.94, el*0.94,
                                     heat*0.94, dist_heating*0.94, others*0.94],
                             texttemplate="%{value:.1f}",
                             name="Emissions profile by 2030 in {} (Kg of CO2-eq)".format(mun)), 1, 2)
        fig.update_layout(title_text='Emissions profile in {} (per-capita KG of CO2-eq)'.format(mun))
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                          marker=dict(line=dict(color='#000000', width=1)))

        return [fig, diet, share_currentmixbus, share_currentmixcar, dwell_unchanged]

@app.callback(
        [Output("cost-CBE-graph", "figure")],
        [Input("municipality-dropdown", "value"), Input("slider-1", "value"), Input("slider-2", "value"),
         Input("slider-3", "value"), Input("slider-4", "value"), Input("slider-5", "value"), Input("slider-6", "value"),
         Input("slider-7", "value"), Input("slider-8", "value"), Input("slider-13", "value"),
         Input("slider-14", "value"), Input("slider-15", "value"), Input("slider-16", "value"),
         Input("slider-18", "value"), Input("slider-9", "value"), Input("slider-10", "value"),
         Input("slider-11", "value"), Input("slider-12", "value"), Input("slider-17", "value"),
         Input("slider-19", "value"), Input("slider-20", "value"), Input("slider-21", "value"),
         Input("slider-22", "value"), Input("slider-25", "value"), Input("slider-24", "value"),
         Input("slider-26", "value"), Input("slider-23", "value"), Input("actors-dropdown-list", "value")]
)
def CBE_costplot(mun, vegan, veg, meat, nutrition, diet, reduction_clothes, doubling_clothes, half_furn, red_air,
                  double_life, package_holidays, rh_share, cars_givenup, share_elbus, share_HVObus, share_currentmixbus,
                  share_hibHVObus, share_elcars, share_currentmixcar, share_plugincar, share_hydrcar, BATel, dwell_unchanged,
                  dwell_20C, dwell_SN, dh_red, actors):

    if dh_red is None:
        dh_red = 0
    if dwell_unchanged is None:
        dwell_unchanged = 0
    if dwell_20C is None:
        dwell_20C = 0
    if dwell_SN is None:
        dwell_SN = 0
    if share_hydrcar is None:
        share_hydrcar = 0
    if share_plugincar is None:
        share_plugincar = 0
    if share_currentmixcar is None:
        share_currentmixcar = 0
    if share_elcars is None:
        share_elcars = 0
    if reduction_clothes is None:
        reduction_clothes = 0
    if doubling_clothes is None:
        doubling_clothes = 0
    if half_furn is None:
        half_furn = 0
    if red_air is None:
        red_air = 0
    if double_life is None:
        double_life = 0
    if package_holidays is None:
        package_holidays = 0
    if rh_share is None:
        rh_share = 0
    if cars_givenup is None:
        cars_givenup = 0
    if nutrition is None:
        nutrition = 0
    if diet is None:
        diet = 0
    if meat is None:
        meat = 0
    if veg is None:
        veg = 0
    if vegan is None:
        vegan = 0
    if share_elbus is None:
        share_elbus = 0
    if share_currentmixbus is None:
        share_currentmixbus = 0
    if share_HVObus is None:
        share_HVObus = 0
    if share_hibHVObus is None:
        share_hibHVObus = 0
    if BATel is None:
        BATel = 0

    share_currentmixbus = 100 - share_elbus - share_HVObus - share_hibHVObus
    diet = 100 - vegan - veg - meat - nutrition
    share_currentmixcar = 100 - share_elcars - share_plugincar - share_hydrcar - cars_givenup
    dwell_unchanged = 100-max([dwell_unchanged, dwell_20C])

    if mun is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select a municipality from the list above.",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return [go.Figure(data=fig)]

    elif actors is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select an actor from the list above.",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return [go.Figure(data=fig)]


    pop_growth = pop.loc[str(mun), 2030]/pop.loc[str(mun), 2019]
    pop_car_ratio = pop.loc[str(mun), 2019]/cars.loc[str(mun), "Number of cars"]
    cars_2030 = pop_growth * cars.loc[str(mun), "Number of cars"]
    bus_capacity = 130
    buses_2030 = pop_growth * buses.loc[str(mun), "Total"]
    total_buses_2030 = buses_2030 + ((cars_givenup/100) * cars_2030 * pop_car_ratio) / bus_capacity
    bus_increase = total_buses_2030/buses_2030
    share_diesel_bus = buses.loc[str(mun), "Diesel"]/buses.loc[str(mun), "Total"]

    vehicles_costs_nl = ((100 - cars_givenup)/100)*cars.loc[str(mun), "Privates-cars"]*pop_growth*((share_elcars/100)*600000 + (share_hydrcar/100)*775000 + (share_plugincar/100)*580000)/pop.loc[str(mun), 2019]
    vehicles_costs_l = dwellings_ownership.loc[str(mun), "housing cooperatives":"private persons"].sum()*cars.loc[str(mun), "Privates-cars"]*pop_growth*((100 - cars_givenup)/100)*(share_elcars/100)*np.mean([9000, 9995, 9122.67])/(10*(dwellings_tenureship.loc[str(mun), "multi-dwelling buildings, tenant-owned":"one- or two-dwelling buildings, owner-occupied"].sum() + dwellings_tenureship.loc[str(mun), "one- or two-dwelling buildings, tenant-owned"])*pop.loc[str(mun), 2019]) + vehicles_costs_nl
    el_l = (BATel/100)*dwellings_ownership.loc[str(mun), "housing cooperatives":"private persons"].sum()*dwellings_stock.loc[str(mun), "Housing stock"]*(8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30*40)/(pop.loc[str(mun), 2019]*(dwellings_tenureship.loc[str(mun), "multi-dwelling buildings, tenant-owned":"one- or two-dwelling buildings, owner-occupied"].sum() + dwellings_tenureship.loc[str(mun), "one- or two-dwelling buildings, tenant-owned"]))
    heating_l = (dwellings_ownership.loc[str(mun), "housing cooperatives":"private persons"].sum()*(dwell_SN/100)*(dwellings_size.loc[str(mun), "1-2 dwelling"]*((1.03*679*0.24) + ((1283 + 1256)*0.84) + (1367 + 7895)*0.15)) + dwellings_ownership.loc[str(mun), "housing cooperatives":"private persons"].sum()*(dwell_SN/100)*(dwellings_size.loc[str(mun), "Multi-dwelling"]*((0.38*679*0.24) + ((1283 + 1256)*0.51) + (1367 + 7895)*0.13)))/(pop.loc[str(mun), 2019]*(dwellings_tenureship.loc[str(mun), "multi-dwelling buildings, tenant-owned":"one- or two-dwelling buildings, owner-occupied"].sum() + dwellings_tenureship.loc[str(mun), "one- or two-dwelling buildings, tenant-owned"]))
    public_transport = ((((cars_givenup/100)*cars_2030*pop_car_ratio/bus_capacity) + buses_2030)*((share_elbus/100)*np.mean([5600000, 4730000, 4400000]) + (share_hibHVObus/100)*2614737) + (((cars_givenup/100)*cars_2030*pop_car_ratio/bus_capacity) + buses_2030)*(share_elbus/100)*((414990/2) + (912978/20) + (190895/20) + (3319920/20)))/pop.loc[str(mun), 2019]
    vehicles_mhc = dwellings_ownership.loc[str(mun), "state, municipal, region"]*cars.loc[str(mun), "Privates-cars"]*pop_growth*((100 - cars_givenup)/100)*((share_elcars)/100)*np.mean([9000, 9995, 9122.67])/(10*pop.loc[str(mun), 2019])
    el_mhc = (BATel/100)*dwellings_ownership.loc[str(mun), "state, municipal, region"]*dwellings_stock.loc[str(mun), "Housing stock"]*(8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30*40)/pop.loc[str(mun), 2019]
    heating_mhc = (dwellings_ownership.loc[str(mun), "state, municipal, region"]*(dwell_SN/100)*(dwellings_size.loc[str(mun), "1-2 dwelling"]*((1.03*679*0.24) + ((1283 + 1256)*0.84) + (1367 + 7895)*0.15)) + dwellings_ownership.loc[str(mun), "state, municipal, region"]*(dwell_SN/100)*(dwellings_size.loc[str(mun), "Multi-dwelling"]*((0.38*679*0.24) + ((1283 + 1256)*0.51) + (1367 + 7895)*0.13)))/pop.loc[str(mun), 2019]
    vehicles_costs_pc = dwellings_ownership.loc[str(mun), "Swedish joint-stock companies":"other owners"].sum()*cars.loc[str(mun), "Privates-cars"]*pop_growth*((100 - cars_givenup)/100)*(share_elcars/100)*np.mean([9000, 9995, 9122.67])/(10*pop.loc[str(mun), 2019]) + ((100 - cars_givenup)/100)*cars.loc[str(mun), "JP-cars"]*pop_growth*((share_elcars/100)*600000 + (share_hydrcar/100)*775000 + (share_plugincar/100)*580000)/pop.loc[str(mun), 2019]
    heating_pc = (dwellings_ownership.loc[str(mun), "Swedish joint-stock companies"]*(dwell_SN/100)*(dwellings_size.loc[str(mun), "1-2 dwelling"]*((1.03*679*0.24) + ((1283 + 1256)*0.84) + (1367 + 7895)*0.15)) + dwellings_ownership.loc[str(mun), "Swedish joint-stock companies"]*(dwell_SN/100)*(dwellings_size.loc[str(mun), "Multi-dwelling"]*((0.38*679*0.24) + ((1283 + 1256)*0.51) + (1367 + 7895)*0.13)))/pop.loc[str(mun), 2019]
    el_pc = (BATel/100)*dwellings_ownership.loc[str(mun), "Swedish joint-stock companies"]*dwellings_stock.loc[str(mun), "Housing stock"]*(8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30*40)/pop.loc[str(mun), 2019]
    vehicles_mun = np.mean([9000, 9995, 9122.67])*((100 - cars_givenup)/100)*(share_elcars/100)*cars_2030/(10*pop.loc[str(mun), 2019])

    vehicles_total = cars.loc[str(mun), "Number of cars"]*pop_growth*((100 - cars_givenup)/100)*(share_elcars/100)*np.mean([9000, 9995, 9122.67])/(10*pop.loc[str(mun), 2019]) + ((100 - cars_givenup)/100)*cars.loc[str(mun), "Number of cars"]*pop_growth*((share_elcars/100)*600000 + (share_hydrcar/100)*775000 + (share_plugincar/100)*580000)/pop.loc[str(mun), 2019]
    el_total = (BATel/100)*dwellings_stock.loc[str(mun), "Housing stock"]*(8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30*40)/(pop.loc[str(mun), 2019])
    heating_total = ((dwell_SN/100)*(dwellings_size.loc[str(mun), "1-2 dwelling"]*((1.03*679*0.24) + ((1283 + 1256)*0.84) + (1367 + 7895)*0.15)) + (dwell_SN/100)*(dwellings_size.loc[str(mun), "Multi-dwelling"]*((0.38*679*0.24) + ((1283 + 1256)*0.51) + (1367 + 7895)*0.13)))/pop.loc[str(mun), 2019]


    hrz = ["Total", "Food", "Clothing", "Housing", "Health", "Air transport", "Recreation",
           "Restaurants and hotels", "Public transport", "Vehicles", "Electricity", "Heating", "District heating",
           "Others"]
    for i in [vehicles_costs_l, vehicles_costs_l, el_l, heating_l, public_transport, vehicles_mhc, el_mhc, heating_mhc,
              el_mhc, heating_mhc, vehicles_costs_pc, heating_pc, el_pc, vehicles_mun]:
        i = locale.format_string("%d", i, grouping = True)

    if actors == "Privates - tenants":

        total = vehicles_costs_nl
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, 0, -vehicles_costs_nl, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Privates - landlords and homeowners":

        total = vehicles_costs_l + el_l + heating_l
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, 0, -vehicles_costs_l, -el_l, -heating_l, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Public transport company":

        total = public_transport
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, -public_transport, 0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality housing company":
        total = vehicles_mhc + el_mhc + heating_mhc
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, 0, -vehicles_mhc, -el_mhc, -heating_mhc, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Utility company":
        total = 0
        vrt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Private businesses":
        total = vehicles_costs_pc + heating_pc + el_pc
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, 0, -vehicles_costs_pc, -el_pc, -heating_pc, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality":
        total = vehicles_mun
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, 0, -vehicles_mun, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Total":
        total = vehicles_total + el_total + heating_total + public_transport
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, -public_transport, -vehicles_total, -el_total, -heating_total, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

@app.callback(
        [Output("opex-CBE-graph", "figure")],
        [Input("municipality-dropdown", "value"), Input("slider-1", "value"), Input("slider-2", "value"),
         Input("slider-3", "value"), Input("slider-4", "value"), Input("slider-5", "value"), Input("slider-6", "value"),
         Input("slider-7", "value"), Input("slider-8", "value"), Input("slider-13", "value"),
         Input("slider-14", "value"), Input("slider-15", "value"), Input("slider-16", "value"),
         Input("slider-18", "value"), Input("slider-9", "value"), Input("slider-10", "value"),
         Input("slider-11", "value"), Input("slider-12", "value"), Input("slider-17", "value"),
         Input("slider-19", "value"), Input("slider-20", "value"), Input("slider-21", "value"),
         Input("slider-22", "value"), Input("slider-25", "value"), Input("slider-24", "value"),
         Input("slider-26", "value"), Input("slider-23", "value"), Input("actors-dropdown-list", "value")]
)
def opex_CBE_costplot(mun, vegan, veg, meat, nutrition, diet, reduction_clothes, doubling_clothes, half_furn, red_air,
                  double_life, package_holidays, rh_share, cars_givenup, share_elbus, share_HVObus, share_currentmixbus,
                  share_hibHVObus, share_elcars, share_currentmixcar, share_plugincar, share_hydrcar, BATel, dwell_unchanged,
                  dwell_20C, dwell_SN, dh_red, actors):

    if dh_red is None:
        dh_red = 0
    if dwell_unchanged is None:
        dwell_unchanged = 0
    if dwell_20C is None:
        dwell_20C = 0
    if dwell_SN is None:
        dwell_SN = 0
    if share_hydrcar is None:
        share_hydrcar = 0
    if share_plugincar is None:
        share_plugincar = 0
    if share_currentmixcar is None:
        share_currentmixcar = 0
    if share_elcars is None:
        share_elcars = 0
    if reduction_clothes is None:
        reduction_clothes = 0
    if doubling_clothes is None:
        doubling_clothes = 0
    if half_furn is None:
        half_furn = 0
    if red_air is None:
        red_air = 0
    if double_life is None:
        double_life = 0
    if package_holidays is None:
        package_holidays = 0
    if rh_share is None:
        rh_share = 0
    if cars_givenup is None:
        cars_givenup = 0
    if nutrition is None:
        nutrition = 0
    if diet is None:
        diet = 0
    if meat is None:
        meat = 0
    if veg is None:
        veg = 0
    if vegan is None:
        vegan = 0
    if share_elbus is None:
        share_elbus = 0
    if share_currentmixbus is None:
        share_currentmixbus = 0
    if share_HVObus is None:
        share_HVObus = 0
    if share_hibHVObus is None:
        share_hibHVObus = 0
    if BATel is None:
        BATel = 0

    if mun is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select a municipality from the list above.",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return [go.Figure(data=fig)]

    elif actors is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select an actor from the list above.",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return [go.Figure(data=fig)]

    share_currentmixbus = 100 - share_elbus - share_HVObus - share_hibHVObus
    diet = 100 - vegan - veg - meat - nutrition
    share_currentmixcar = 100 - share_elcars - share_plugincar - share_hydrcar - cars_givenup
    dwell_unchanged = 100-max([dwell_unchanged, dwell_20C])

    pop_growth = pop.loc[str(mun), 2030] / pop.loc[str(mun), 2019]
    pop_car_ratio = pop.loc[str(mun), 2019] / cars.loc[str(mun), "Number of cars"]
    cars_2030 = pop_growth * cars.loc[str(mun), "Number of cars"]
    bus_capacity = 130
    buses_2030 = pop_growth * buses.loc[str(mun), "Total"]
    total_buses_2030 = buses_2030 + ((cars_givenup / 100) * cars_2030 * pop_car_ratio / bus_capacity)
    bus_increase = total_buses_2030 / buses_2030
    share_diesel_bus = buses.loc[str(mun), "Diesel"] / buses.loc[str(mun), "Total"]
    regional_pop = reg_pop.loc[regions.loc[str(mun)], "Pop"]
    mun_share = pop.loc[str(mun), 2019]/regional_pop

#The opex on public transport for the public transport company will be the last one analyzed as it entails some complicated assumptions
    opex_vehicles_nl = float(pop_growth*cars.loc[str(mun), "Privates-cars"]*(100 - cars_givenup)*(0.01)*(((share_elcars/100)*0.861586*0.221*distance.loc[str(mun)] + (share_elcars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (share_hydrcar/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((share_plugincar/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (share_elcars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_pt_nl = float(pt_cost.loc[regions.loc[str(mun)], "Annual cost"]*12*(cars_givenup/100)*cars_2030*pop_car_ratio/pop.loc[str(mun), 2019:2030].sum())
    opex_vehicles_l = float(pop_growth*cars.loc[str(mun), "Privates-cars"]*(100 - cars_givenup)*(0.01)*(((share_elcars/100)*0.861586*0.221*distance.loc[str(mun)] + (share_elcars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (share_hydrcar/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((share_plugincar/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (share_elcars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_pt_l = float(pt_cost.loc[regions.loc[str(mun)], "Annual cost"] * 12 * (cars_givenup / 100) * cars_2030 * pop_car_ratio / pop.loc[str(mun), 2019:2030].sum())
    opex_district_heating = (dh_red/100)*(dh.loc[str(mun), "Stenkol (GWh)":"Övrigt fossilt bränsle (GWh)"].sum() + dh.loc[str(mun), "Flue gas condensation energy of fossil origin (GWh)"])*1000*(211849 + 6)/pop.loc[str(mun), 2019].sum()
    opex_vehicles_pb = float(pop_growth*cars.loc[str(mun), "JP-cars"]*(100 - cars_givenup)*(0.01)*(((share_elcars/100)*0.861586*0.221*distance.loc[str(mun)] + (share_elcars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (share_hydrcar/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((share_plugincar/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (share_elcars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_public_transport = float((bus_increase*offered_pt.loc[regions.loc[str(mun)], "Distance"]*mun_share*((share_elbus/100)*(3.3 + 0.82*1.053) + ((share_hibHVObus + share_HVObus)/100)*(3 + 3.6*3.5)) + total_buses_2030*(share_elbus/100)*4000*470/12)*12/pop.loc[str(mun), 2019:2030].sum())

    opex_vehicles_total =  float(pop_growth*cars.loc[str(mun), "Number of cars"]*(100 - cars_givenup)*(0.01)*(((share_elcars/100)*0.861586*0.221*distance.loc[str(mun)] + (share_elcars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (share_hydrcar/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((share_plugincar/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (share_elcars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_pt_total = float(pt_cost.loc[regions.loc[str(mun)], "Annual cost"]*12*(cars_givenup/100)*cars_2030*pop_car_ratio/pop.loc[str(mun), 2019:2030].sum()) + float((bus_increase*offered_pt.loc[regions.loc[str(mun)], "Distance"]*mun_share*((share_elbus/100)*(3.3 + 0.82*1.053) + ((share_hibHVObus + share_HVObus)/100)*(3 + 3.6*3.5)) + total_buses_2030*(share_elbus/100)*4000*470/12)*12/pop.loc[str(mun), 2019:2030].sum())



    hrz = ["Total", "Food", "Clothing", "Housing", "Health", "Air transport", "Recreation",
           "Restaurants and hotels", "Public transport", "Vehicles", "Electricity", "Heating", "District heating",
           "Others"]

    if actors == "Privates - tenants":

        total = opex_vehicles_nl + opex_pt_nl
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, -opex_pt_nl, -opex_vehicles_nl, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Privates - landlords and homeowners":

        total = opex_vehicles_l + opex_pt_l
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, -opex_pt_l, -opex_vehicles_l, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Public transport company":

        total = opex_public_transport
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, -opex_public_transport, 0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality housing company":
        total = 0
        vrt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Utility company":
        total = opex_district_heating
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -opex_district_heating, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Private businesses":
        total = opex_vehicles_pb
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, 0, -opex_vehicles_pb, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality":
        total = 0
        vrt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Total":
        total = opex_vehicles_total + opex_pt_total + opex_district_heating
        vrt = [total, 0, 0, 0, 0, 0, 0, 0, -opex_pt_total, -opex_vehicles_total, 0, 0, -opex_district_heating, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

@app.callback(
    [Output("results-graph-2", "figure"), Output("slider-29", "value"), Output("slider-34", "value"),
     Output("slider-38", "value")],
    [Input("municipality-dropdown", "value"), Input("slider-27", "value"), Input("slider-28", "value"),
     Input("slider-29", "value"), Input("slider-30", "value"), Input("slider-31", "value"), Input("slider-32", "value"),
     Input("slider-33", "value"), Input("slider-34", "value"), Input("slider-35", "value"), Input("slider-36", "value"),
     Input("slider-37", "value"), Input("slider-38", "value"), Input("slider-39", "value"), Input("slider-40", "value"),
     Input("scenario-dropdown-list-2", "value"), Input("slider-41", "value")]
)
def render_page_3(mun, el_bus, hvo_bus, current_fuel_bus, hHVO_bus, air_transp, el_car, pt_car, current_fuel_car, ph_car,
                  BAT_appl, ind_temp_red, no_heat_measure, sn_measure, LGB_heavy_trucks, scenario, hydr_car):
    if mun is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select a municipality before proceeding",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return[go.Figure(data=fig), current_fuel_bus, current_fuel_car, no_heat_measure]

    if el_bus is None:
        el_bus = 0
    if hvo_bus is None:
        hvo_bus = 0
    if hHVO_bus is None:
        hHVO_bus = 0
    if air_transp is None:
        air_transp = 0
    if el_car is None:
        el_car = 0
    if pt_car is None:
        pt_car = 0
    if ph_car is None:
        ph_car = 0
    if BAT_appl is None:
        BAT_appl = 0
    if ind_temp_red is None:
        ind_temp_red = 0
    if sn_measure is None:
        sn_measure = 0
    if LGB_heavy_trucks is None:
        LGB_heavy_trucks = 0
    if hydr_car is None:
        hydr_car = 0

    current_fuel_bus = 100 - el_bus - hvo_bus - hHVO_bus
    current_fuel_car = 100 - el_car - pt_car - ph_car - hydr_car
    no_heat_measure = 100 - max([ind_temp_red, sn_measure])

    transport = ((el_car/100)*((0.027)*(cars.loc[str(mun), "Cars-diesel"]/cars.loc[str(mun), "Number of cars"]) + (0.019)*(cars.loc[str(mun), "Cars-petrol"]/cars.loc[str(mun), "Number of cars"])) + (current_fuel_car/100) + (ph_car/100)*((0.39)*(cars.loc[str(mun), "Cars-diesel"]/cars.loc[str(mun), "Number of cars"]) + (0.028)*(cars.loc[str(mun), "Cars-petrol"]/cars.loc[str(mun), "Number of cars"])) + (hydr_car/100)*((0.73)*(cars.loc[str(mun), "Cars-diesel"]/cars.loc[str(mun), "Number of cars"]) + (0.52)*(cars.loc[str(mun), "Cars-petrol"]/cars.loc[str(mun), "Number of cars"])))*tbe_emissions.loc[str(mun), "Passenger cars"] + ((LGB_heavy_trucks/100)*0.18*(cars.loc[str(mun), "HL- diesel"]/cars.loc[str(mun), "Heavy lorries"]) + (1 - LGB_heavy_trucks/100)*(cars.loc[str(mun), "HL- diesel"]/cars.loc[str(mun), "Heavy lorries"]))*tbe_emissions.loc[str(mun), "Heavy trucks"] + tbe_emissions.loc[str(mun), "Light trucks"] + ((el_bus/100)*0.076 + (hvo_bus/100)*0.3 + (hHVO_bus/100)*0.16 + (current_fuel_bus/100))*tbe_emissions.loc[str(mun), "Buses"] + (100 -air_transp)/(100)*tbe_emissions.loc[str(mun), "Domestic air traffic"] + tbe_emissions.loc[str(mun), "Mopeds and Motorcycles"] + tbe_emissions.loc[str(mun), "Wear and tear from tires and brakes": "Domestic civil shipping (incl. private pleasure craft)"].sum() + tbe_emissions.loc[str(mun), "Railway":"Military transport"].sum()
    industry = tbe_emissions.loc[str(mun), "Industry (energy + processes)"]
    agriculture = tbe_emissions.loc[str(mun), "Animal digestion":"Other fertilizers"].sum()
    el_dh = tbe_emissions.loc[str(mun), "Electricity and district heating"]*(el_shares.loc[str(mun), "El share"]*((BAT_appl/100)*0.2075 + (100 - BAT_appl)/100) + (1 - el_shares.loc[str(mun), "El share"])*((ind_temp_red/100)*0.21*dwellings_ratio.loc[str(mun), "1,2 Dwellings"] + (ind_temp_red/100)*0.27*dwellings_ratio.loc[str(mun), "Multiple dwellings"] + (sn_measure/100)*0.26*dwellings_ratio.loc[str(mun), "1,2 Dwellings"] + (sn_measure/100)*0.27*dwellings_ratio.loc[str(mun), "Multiple dwellings"] + (no_heat_measure/100)))
    own_heating = tbe_emissions.loc[str(mun), "Housing":"Agricultural and forestry premises"].sum()
    work_machines = tbe_emissions.loc[str(mun), "Scooters and quad bikes":"Other (airports, ports, m.m.)"].sum()
    product_use = tbe_emissions.loc[str(mun), "Solvent use - operations":"Other product use"].sum()
    waste = tbe_emissions.loc[str(mun), "Landfills":"Other waste management"].sum()
    foreign_transport = tbe_emissions.loc[str(mun), "Foreign shipping within Sweden's borders": "International flights below 1000 m altitude in Swedish airspace"].sum()

    transport = 1000*transport/pop.loc[str(mun), 2019]
    industry = 1000*industry/pop.loc[str(mun), 2019]
    agriculture = 1000*agriculture/pop.loc[str(mun), 2019]
    el_dh = 1000*el_dh/pop.loc[str(mun), 2019]
    own_heating = 1000*own_heating/pop.loc[str(mun), 2019]
    work_machines = 1000*work_machines/pop.loc[str(mun), 2019]
    product_use = 1000*product_use/pop.loc[str(mun), 2019]
    waste = 1000*waste/pop.loc[str(mun), 2019]
    foreign_transport = 1000*foreign_transport/pop.loc[str(mun), 2019]

    total = transport + industry + agriculture + el_dh + own_heating + work_machines + product_use + waste + foreign_transport

    transport_2019 =  1000*(tbe_emissions.loc[str(mun), "Passenger cars"] + tbe_emissions.loc[str(mun), "Heavy trucks"] + tbe_emissions.loc[str(mun), "Light trucks"] + tbe_emissions.loc[str(mun), "Buses"] + tbe_emissions.loc[str(mun), "Domestic air traffic"] + tbe_emissions.loc[str(mun), "Mopeds and Motorcycles"] + tbe_emissions.loc[str(mun), "Wear and tear from tires and brakes": "Domestic civil shipping (incl. private pleasure craft)"].sum() + tbe_emissions.loc[str(mun), "Railway":"Military transport"].sum())/pop.loc[str(mun), 2019]
    industry_2019 = 1000*tbe_emissions.loc[str(mun), "Industry (energy + processes)"]/pop.loc[str(mun), 2019]
    agriculture_2019 = 1000*tbe_emissions.loc[str(mun), "Animal digestion":"Other fertilizers"].sum()/pop.loc[str(mun), 2019]
    el_dh_2019 = 1000*tbe_emissions.loc[str(mun), "Electricity and district heating"]/pop.loc[str(mun), 2019]
    own_heating_2019 = 1000*tbe_emissions.loc[str(mun), "Housing":"Agricultural and forestry premises"].sum()/pop.loc[str(mun), 2019]
    work_machines_2019 = 1000*tbe_emissions.loc[str(mun), "Scooters and quad bikes":"Other (airports, ports, m.m.)"].sum()/pop.loc[str(mun), 2019]
    product_use_2019 = 1000*tbe_emissions.loc[str(mun), "Solvent use - operations":"Other product use"].sum()/pop.loc[str(mun), 2019]
    waste_2019 = 1000*tbe_emissions.loc[str(mun), "Landfills":"Other waste management"].sum()/pop.loc[str(mun), 2019]
    foreign_transport_2019 = 1000*tbe_emissions.loc[str(mun), "Foreign shipping within Sweden's borders": "International flights below 1000 m altitude in Swedish airspace"].sum()/pop.loc[str(mun), 2019]

    total_2019 = transport_2019 + industry_2019 + agriculture_2019 + el_dh_2019 + own_heating_2019 + work_machines_2019 + product_use_2019 + waste_2019 + foreign_transport_2019
    plot_data = pd.DataFrame([transport, industry, agriculture, el_dh, own_heating, work_machines, product_use,
                              waste, foreign_transport, transport*1.1683, industry*1.1683, agriculture*1.1683,
                              el_dh*1.1683, own_heating*1.1683, work_machines*1.1683, product_use*1.1683, waste*1.1683,
                              foreign_transport*1.1683, transport*0.94, industry*0.94, agriculture*0.94,
                              el_dh*0.94, own_heating*0.94, work_machines*0.94, product_use*0.94, waste*0.94,
                              foreign_transport*0.94], columns=["Var"])

    if scenario == "BAU Scenario":
        hrz = ["Transport", "Industry", "Agriculture", "Electricity and DH",
               "Own heating", "Work machinery", "Product use", "Waste", "Foreign transport"]
        fig = make_subplots(1, 2, subplot_titles=["2019: {} Kg".format(round(total_2019,2)), "2030: {} Kg".format(round(total,2))],
                            specs=[[{"type": "pie"}, {"type": "pie"}]])
        fig.add_trace(
            go.Pie(labels=hrz, values=[transport_2019, industry_2019, agriculture_2019, el_dh_2019, own_heating_2019,
                                       work_machines_2019, product_use_2019, waste_2019, foreign_transport_2019],
                   texttemplate="%{value:.1f}",
                   name="Emissions profile by 2019 in {} (Kg of CO2-eq)".format(mun)), 1, 1)
        fig.add_trace(go.Pie(labels=hrz,
                             values=[transport, industry, agriculture, el_dh, own_heating, work_machines, product_use,
                                     waste,
                                     foreign_transport], texttemplate="%{value:.1f}",
                             name="Emissions profile by 2030 in {} (Kg of CO2-eq)".format(mun)), 1, 2)
        fig.update_layout(title_text='Emissions profile in {} (per-capita KG of CO2-eq)'.format(mun))
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                          marker=dict(line=dict(color='#000000', width=1)))

        return [fig, current_fuel_bus, current_fuel_car, no_heat_measure]

    elif scenario == "Scenario 2":
        total = transport*1.1683 + industry*1.1683 + agriculture*1.1683 + el_dh*1.1683 + own_heating*1.1683 + work_machines*1.1683 + product_use*1.1683 + waste*1.1683 + foreign_transport*1.1683

        hrz = ["Total", "Transport", "Industry", "Agriculture", "Electricity and DH",
               "Own heating", "Work machinery", "Product use", "Waste", "Foreign transport"]
        fig = make_subplots(1, 2, subplot_titles=["2019: {} Kg".format(round(total_2019,2)), "2030: {} Kg".format(round(total,2))],
                            specs=[[{"type": "pie"}, {"type": "pie"}]])
        fig.add_trace(
            go.Pie(labels=hrz, values=[transport_2019, industry_2019, agriculture_2019, el_dh_2019, own_heating_2019,
                                       work_machines_2019, product_use_2019, waste_2019, foreign_transport_2019],
                   texttemplate="%{value:.1f}",
                   name="Emissions profile by 2019 in {} (Kg of CO2-eq)".format(mun)), 1, 1)
        fig.add_trace(go.Pie(labels=hrz,
                             values=[transport*1.1683, industry*1.1683, agriculture*1.1683, el_dh*1.1683, own_heating*1.1683,
                                     work_machines*1.1683, product_use*1.1683, waste*1.1683, foreign_transport*1.1683],
                             texttemplate="%{value:.1f}", name="Emissions profile by 2030 in {} (Kg of CO2-eq)".format(mun)), 1, 2)
        fig.update_layout(title_text='Emissions profile in {} (per-capita KG of CO2-eq)'.format(mun))
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                          marker=dict(line=dict(color='#000000', width=1)))
        return [fig, current_fuel_bus, current_fuel_car, no_heat_measure]

    elif scenario == "Scenario 3":
        total = transport*0.94 + industry*0.94 + agriculture*0.94 + el_dh*0.94 + own_heating*0.94 + work_machines*0.94 + product_use*0.94 + waste*0.94 + foreign_transport*0.94

        hrz = ["Total", "Transport", "Industry", "Agriculture", "Electricity and DH",
               "Own heating", "Work machinery", "Product use", "Waste", "Foreign transport"]
        fig = make_subplots(1, 2, subplot_titles=["2019: {} Kg".format(round(total_2019, 2)),
                                                  "2030: {} Kg".format(round(total, 2))],
                            specs=[[{"type": "pie"}, {"type": "pie"}]])
        fig.add_trace(
            go.Pie(labels=hrz, values=[transport_2019, industry_2019, agriculture_2019, el_dh_2019, own_heating_2019,
                                       work_machines_2019, product_use_2019, waste_2019, foreign_transport_2019],
                   texttemplate="%{value:.1f}",
                   name="Emissions profile by 2019 in {} (Kg of CO2-eq)".format(mun)), 1, 1)
        fig.add_trace(go.Pie(labels=hrz,
                             values=[transport*0.94, industry*0.94, agriculture*0.943, el_dh*0.94,
                                     own_heating*0.94,
                                     work_machines*0.94, product_use*0.94, waste*0.94,
                                     foreign_transport*0.94],
                             texttemplate="%{value:.1f}",
                             name="Emissions profile by 2030 in {} (Kg of CO2-eq)".format(mun)), 1, 2)
        fig.update_layout(title_text='Emissions profile in {} (per-capita KG of CO2-eq)'.format(mun))
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                          marker=dict(line=dict(color='#000000', width=1)))
        return [fig, current_fuel_bus, current_fuel_car, no_heat_measure]

@app.callback(
    [Output("CAPEX-TBE-graph", "figure")],
    [Input("municipality-dropdown", "value"), Input("actors-dropdown-list-2", "value"), Input("scenario-dropdown-list-2", "value"),
     Input("slider-27", "value"), Input("slider-28", "value"), Input("slider-29", "value"), Input("slider-30", "value"),
     Input("slider-31", "value"), Input("slider-32", "value"), Input("slider-33", "value"), Input("slider-34", "value"),
     Input("slider-35", "value"), Input("slider-36", "value"), Input("slider-37", "value"), Input("slider-38", "value"),
     Input("slider-39", "value"), Input("slider-40", "value"), Input("slider-41", "value")]
)
def CAPEX_tbe_costplot(mun, actors, scenario, el_buses, HVO_buses, currentmix_buses, hybridHVO_buses, air_reduction, el_cars,
                       cars_givenup, currentmix_cars, pluginhybrid_cars, BAT_appls, indoor_temp, noheatmeasure, SN,
                       LGB_trucks, hydrogen_cars):

    if el_buses is None:
        el_buses = 0
    if HVO_buses is None:
        HVO_buses = 0
    if currentmix_buses is None:
        currentmix_buses = 0
    if hybridHVO_buses is None:
        hybridHVO_buses = 0
    if air_reduction is None:
        air_reduction = 0
    if el_cars is None:
        el_cars = 0
    if cars_givenup is None:
        cars_givenup = 0
    if currentmix_cars is None:
        currentmix_cars = 0
    if pluginhybrid_cars is None:
        pluginhybrid_cars = 0
    if BAT_appls is None:
        BAT_appls = 0
    if indoor_temp is None:
        indoor_temp = 0
    if noheatmeasure is None:
        noheatmeasure = 0
    if SN is None:
        SN = 0
    if LGB_trucks is None:
        LGB_trucks = 0
    if hydrogen_cars is None:
        hydrogen_cars = 0

    currentmix_buses = 100 - el_buses - HVO_buses - hybridHVO_buses
    currentmix_cars = 100 - el_cars - cars_givenup - pluginhybrid_cars - hydrogen_cars
    noheatmeasure = 100 - max([indoor_temp, SN])

    if mun is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select a municipality before proceeding",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return[go.Figure(data=fig)]

    elif actors is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select an actor before proceeding",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return [go.Figure(data=fig)]

    pop_growth = pop.loc[str(mun), 2030] / pop.loc[str(mun), 2019]
    pop_car_ratio = pop.loc[str(mun), 2019] / cars.loc[str(mun), "Number of cars"]
    cars_2030 = pop_growth * cars.loc[str(mun), "Number of cars"]
    bus_capacity = 130
    buses_2030 = pop_growth * buses.loc[str(mun), "Total"]
    total_buses_2030 = buses_2030 + ((cars_givenup / 100) * cars_2030 * pop_car_ratio) / bus_capacity
    bus_increase = total_buses_2030 / buses_2030
    share_diesel_bus = buses.loc[str(mun), "Diesel"] / buses.loc[str(mun), "Total"]

    vehicles_pnl = cars.loc[str(mun), "Privates-cars"]*pop_growth*(1 - cars_givenup/100)*((el_cars/100)*595720 + (pluginhybrid_cars/100)*587905 + (hydrogen_cars/100)*774900)/pop.loc[str(mun), 2019]
    vehicles_pl = dwellings_ownership.loc[str(mun), "housing cooperatives":"private persons"].sum() * cars.loc[str(mun), "Privates-cars"] * pop_growth * ((100 - cars_givenup) / 100) * (el_cars / 100) * np.mean([9000, 9995, 9122.67]) / (10 * (dwellings_tenureship.loc[str(mun),"multi-dwelling buildings, tenant-owned":"one- or two-dwelling buildings, owner-occupied"].sum() + dwellings_tenureship.loc[str(mun), "one- or two-dwelling buildings, tenant-owned"]) * pop.loc[str(mun), 2019]) + vehicles_pnl
    el_l = (BAT_appls / 100) * dwellings_ownership.loc[str(mun), "housing cooperatives":"private persons"].sum() * dwellings_stock.loc[str(mun), "Housing stock"] * (8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30 * 40) / ( pop.loc[str(mun), 2019] * (dwellings_tenureship.loc[str(mun),"multi-dwelling buildings, tenant-owned":"one- or two-dwelling buildings, owner-occupied"].sum() + dwellings_tenureship.loc[str(mun), "one- or two-dwelling buildings, tenant-owned"]))
    heating_l = (dwellings_ownership.loc[str(mun), "housing cooperatives":"private persons"].sum() * (SN / 100) * (dwellings_size.loc[str(mun), "1-2 dwelling"] * ((1.03 * 679 * 0.24) + ((1283 + 1256) * 0.84) + (1367 + 7895) * 0.15)) + dwellings_ownership.loc[str(mun),"housing cooperatives":"private persons"].sum() * (SN / 100) * (dwellings_size.loc[str(mun), "Multi-dwelling"] * ((0.38 * 679 * 0.24) + ((1283 + 1256) * 0.51) + (1367 + 7895) * 0.13))) / (pop.loc[str(mun), 2019] * (dwellings_tenureship.loc[str(mun),"multi-dwelling buildings, tenant-owned":"one- or two-dwelling buildings, owner-occupied"].sum() +dwellings_tenureship.loc[str(mun), "one- or two-dwelling buildings, tenant-owned"]))
    public_transport = ((((cars_givenup/100)*cars_2030*pop_car_ratio/bus_capacity) + buses_2030)*((el_buses/100)*np.mean([5600000, 4730000, 4400000]) + (hybridHVO_buses/100)*2614737) + (((cars_givenup/100)*cars_2030*pop_car_ratio*el_buses/bus_capacity) + buses_2030)*((414990/2) + (912978/20) + (190895/20) + (3319920/20)))/pop.loc[str(mun), 2019]
    vehicles_mhc = dwellings_ownership.loc[str(mun), "state, municipal, region"]*cars.loc[str(mun), "Privates-cars"]*pop_growth*((100 - cars_givenup)/100)*((el_cars)/100)*np.mean([9000, 9995, 9122.67])/(10*pop.loc[str(mun), 2019])
    el_mhc = (BAT_appls/100)*dwellings_ownership.loc[str(mun), "state, municipal, region"]*dwellings_stock.loc[str(mun), "Housing stock"]*(8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30*40)/pop.loc[str(mun), 2019]
    heating_mhc = (dwellings_ownership.loc[str(mun), "state, municipal, region"]*(SN/100)*(dwellings_size.loc[str(mun), "1-2 dwelling"]*((1.03*679*0.24) + ((1283 + 1256)*0.84) + (1367 + 7895)*0.15)) + dwellings_ownership.loc[str(mun), "state, municipal, region"]*(SN/100)*(dwellings_size.loc[str(mun), "Multi-dwelling"]*((0.38*679*0.24) + ((1283 + 1256)*0.51) + (1367 + 7895)*0.13)))/pop.loc[str(mun), 2019]
    heavy_vehicles_pc = cars.loc[str(mun), "HL- diesel"]*(LGB_trucks/100)*np.mean([2832173.45, 2605100.5])/pop.loc[str(mun), 2019]
    vehicles_mun = np.mean([9000, 9995, 9122.67])*((100 - cars_givenup)/100)*(el_cars/100)*cars_2030/(10*pop.loc[str(mun), 2019])
    vehicles_costs_pc = dwellings_ownership.loc[str(mun), "Swedish joint-stock companies":"other owners"].sum()*cars.loc[str(mun), "Privates-cars"] * pop_growth * ((100 - cars_givenup) / 100) * (el_cars / 100) * np.mean([9000, 9995, 9122.67]) / (10 * pop.loc[str(mun), 2019]) + ((100 - cars_givenup) / 100) * cars.loc[str(mun), "JP-cars"] * pop_growth * ((el_cars / 100) * 600000 + (hydrogen_cars / 100) * 775000 + (pluginhybrid_cars / 100) * 580000) / pop.loc[str(mun), 2019]
    heating_pc = (dwellings_ownership.loc[str(mun), "Swedish joint-stock companies"] * (SN / 100) * (dwellings_size.loc[str(mun), "1-2 dwelling"] * ((1.03 * 679 * 0.24) + ((1283 + 1256) * 0.84) + (1367 + 7895) * 0.15)) + dwellings_ownership.loc[str(mun), "Swedish joint-stock companies"] * (SN/ 100) * (dwellings_size.loc[str(mun), "Multi-dwelling"] * ((0.38 * 679 * 0.24) + ((1283 + 1256) * 0.51) + (1367 + 7895) * 0.13))) / pop.loc[str(mun), 2019]
    el_pc = (BAT_appls / 100) * dwellings_ownership.loc[str(mun), "Swedish joint-stock companies"] * dwellings_stock.loc[str(mun), "Housing stock"] * (8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30 * 40) / pop.loc[str(mun), 2019]

    personal_vehicles_total = cars.loc[str(mun), "Number of cars"]*pop_growth*(1 - cars_givenup/100)*((el_cars/100)*595720 + (pluginhybrid_cars/100)*587905 + (hydrogen_cars/100)*774900)/pop.loc[str(mun), 2019]
    el_total = (BAT_appls / 100) * dwellings_stock.loc[str(mun), "Housing stock"] * (8990 + 13950 + 11500 + 12100 + 20347 + 14770 + 30 * 40) / ( pop.loc[str(mun), 2019])
    heating_total = ((SN / 100) * (dwellings_size.loc[str(mun), "1-2 dwelling"] * ((1.03 * 679 * 0.24) + ((1283 + 1256) * 0.84) + (1367 + 7895) * 0.15)) + (SN / 100) * (dwellings_size.loc[str(mun), "Multi-dwelling"] * ((0.38 * 679 * 0.24) + ((1283 + 1256) * 0.51) + (1367 + 7895) * 0.13))) / (pop.loc[str(mun), 2019])


    hrz = ["Total", "Personal vehicles", "Heavy trucks", "Public transport", "Electricity and heating"]

    if actors == "Privates - tenants":

        total = vehicles_pnl
        vrt = [total, -vehicles_pnl, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Privates - landlords and homeowners":

        total = vehicles_pl + el_l + heating_l
        vrt = [total, -vehicles_pl, 0, 0, -el_l -heating_l]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Public transport company":

        total = public_transport
        vrt = [total, 0, 0, -public_transport, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality housing company":
        total = vehicles_mhc + el_mhc + heating_mhc
        vrt = [total, -vehicles_mhc, 0, 0, -el_mhc -heating_mhc]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Utility company":
        total = 0
        vrt = [0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Private businesses":
        total = vehicles_costs_pc + heavy_vehicles_pc + el_pc + heating_pc
        vrt = [total, -vehicles_costs_pc, -heavy_vehicles_pc, 0, -el_pc - heating_pc]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality":
        total = vehicles_mun
        vrt = [total, -vehicles_mun, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Total":
        total = personal_vehicles_total + el_total + heating_total + public_transport + heavy_vehicles_pc
        vrt = [total, -personal_vehicles_total, -heavy_vehicles_pc, -public_transport, -el_total -heating_total]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita CAPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

@app.callback(
    [Output("OPEX-TBE-graph", "figure")],
    [Input("municipality-dropdown", "value"), Input("actors-dropdown-list-2", "value"),
     Input("slider-27", "value"), Input("slider-28", "value"), Input("slider-29", "value"), Input("slider-30", "value"),
     Input("slider-31", "value"), Input("slider-32", "value"), Input("slider-33", "value"), Input("slider-34", "value"),
     Input("slider-35", "value"), Input("slider-36", "value"), Input("slider-37", "value"), Input("slider-38", "value"),
     Input("slider-39", "value"), Input("slider-40", "value"), Input("slider-41", "value")]
)
def OPEX_tbe_costplot(mun, actors, el_buses, HVO_buses, currentmix_buses, hybridHVO_buses, air_reduction, el_cars,
                       cars_givenup, currentmix_cars, pluginhybrid_cars, BAT_appls, indoor_temp, noheatmeasure, SN,
                       LGB_trucks, hydrogen_cars):

    if el_buses is None:
        el_buses = 0
    if HVO_buses is None:
        HVO_buses = 0
    if currentmix_buses is None:
        currentmix_buses = 0
    if hybridHVO_buses is None:
        hybridHVO_buses = 0
    if air_reduction is None:
        air_reduction = 0
    if el_cars is None:
        el_cars = 0
    if cars_givenup is None:
        cars_givenup = 0
    if currentmix_cars is None:
        currentmix_cars = 0
    if pluginhybrid_cars is None:
        pluginhybrid_cars = 0
    if BAT_appls is None:
        BAT_appls = 0
    if indoor_temp is None:
        indoor_temp = 0
    if noheatmeasure is None:
        noheatmeasure = 0
    if SN is None:
        SN = 0
    if LGB_trucks is None:
        LGB_trucks = 0
    if hydrogen_cars is None:
        hydrogen_cars = 0

    currentmix_buses = 100 - el_buses - HVO_buses - hybridHVO_buses
    currentmix_cars = 100 - el_cars - cars_givenup - pluginhybrid_cars - hydrogen_cars
    noheatmeasure = 100 - max([indoor_temp, SN])

    if mun is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select a municipality before proceeding",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return[go.Figure(data=fig)]

    elif actors is None:
        fig = go.Figure()
        fig.add_annotation(
            x=2.7,
            y=1.8,
            text="Please make sure to select an actor before proceeding",
            showarrow=False,
            font=dict(
                size=20
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
        return [go.Figure(data=fig)]

    pop_growth = pop.loc[str(mun), 2030] / pop.loc[str(mun), 2019]
    pop_car_ratio = pop.loc[str(mun), 2019] / cars.loc[str(mun), "Number of cars"]
    cars_2030 = pop_growth * cars.loc[str(mun), "Number of cars"]
    bus_capacity = 130
    buses_2030 = pop_growth * buses.loc[str(mun), "Total"]
    total_buses_2030 = buses_2030 + ((cars_givenup / 100) * cars_2030 * pop_car_ratio) / bus_capacity
    bus_increase = total_buses_2030 / buses_2030
    share_diesel_bus = buses.loc[str(mun), "Diesel"] / buses.loc[str(mun), "Total"]
    regional_pop = reg_pop.loc[regions.loc[str(mun)], "Pop"]
    mun_share = pop.loc[str(mun), 2019]/regional_pop

    opex_vehicles_nl = float(pop_growth*cars.loc[str(mun), "Privates-cars"]*(100 - cars_givenup)*(0.01)*(((el_cars/100)*0.861586*0.221*distance.loc[str(mun)] + (el_cars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (hydrogen_cars/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((pluginhybrid_cars/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (el_cars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_pt_nl = float(pt_cost.loc[regions.loc[str(mun)], "Annual cost"]*12*(cars_givenup/100)*cars_2030*pop_car_ratio/pop.loc[str(mun), 2019:2030].sum())
    opex_vehicles_l = float(pop_growth*cars.loc[str(mun), "Privates-cars"]*(100 - cars_givenup)*(0.01)*(((el_cars/100)*0.861586*0.221*distance.loc[str(mun)] + (el_cars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (hydrogen_cars/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((pluginhybrid_cars/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (el_cars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_pt_l = float(pt_cost.loc[regions.loc[str(mun)], "Annual cost"] * 12 * (cars_givenup / 100) * cars_2030 * pop_car_ratio / pop.loc[str(mun), 2019:2030].sum())
    opex_vehicles_pb = float(pop_growth*cars.loc[str(mun), "JP-cars"]*(100 - cars_givenup)*(0.01)*(((el_cars/100)*0.861586*0.221*distance.loc[str(mun)] + (el_cars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (hydrogen_cars/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((pluginhybrid_cars/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (el_cars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_heavyvehicles_pb = float((LGB_trucks/100)*((cars.loc[str(mun), "HL- diesel"]/cars.loc[str(mun), "Heavy lorries"]))*pop_growth*cars.loc[str(mun), "Heavy lorries"]*125000*(0.23*13 + 2)*12/pop.loc[str(mun), 2019:2030].sum())
    opex_public_transport = float((bus_increase * offered_pt.loc[regions.loc[str(mun)], "Distance"] * mun_share * ((el_buses / 100) * (3.3 + 0.82 * 1.053) + ((hybridHVO_buses + HVO_buses) / 100) * (3 + 3.6 * 3.5)) + total_buses_2030 * (el_buses / 100) * 4000 * 470 / 12) * 12 / pop.loc[str(mun), 2019:2030].sum())

    opex_vehicles_total = float(pop_growth*cars.loc[str(mun), "Number of cars"]*(100 - cars_givenup)*(0.01)*(((el_cars/100)*0.861586*0.221*distance.loc[str(mun)] + (el_cars/100)*distance.loc[str(mun)]*1659.96*73/150000)*12 + (hydrogen_cars/100)*np.average([29.4, 28.4, 19.4, 27.37])*distance.loc[str(mun)]*0.00875*12 + ((pluginhybrid_cars/100)*0.861586*0.221*distance.loc[str(mun)]*0.46 + (el_cars/100)*distance.loc[str(mun)]*0.46*1659.96*73/150000)*12)/(pop.loc[str(mun), 2019:2030].sum()))
    opex_pt_total = opex_pt_nl + opex_public_transport

    hrz = ["Total", "Personal vehicles", "Heavy trucks", "Public transport", "Electricity and heating"]

    if actors == "Privates - tenants":

        total = opex_vehicles_nl + opex_pt_nl
        vrt = [total, -opex_vehicles_nl, 0, -opex_pt_nl, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Privates - landlords and homeowners":

        total = opex_vehicles_l + opex_pt_l
        vrt = [total, -opex_vehicles_l, 0, -opex_pt_l, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Public transport company":

        total = opex_public_transport
        vrt = [total, 0, 0, -opex_public_transport, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality housing company":
        total = 0
        vrt = [0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Private businesses":
        total = opex_vehicles_pb + opex_heavyvehicles_pb
        vrt = [total, -opex_vehicles_pb, -opex_heavyvehicles_pb, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            totals={"marker": {"color": "#636efa"}},
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Municipality":
        total = 0
        vrt = [0, 0, 0, 0, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

    if actors == "Total":
        total = opex_heavyvehicles_pb + opex_vehicles_total + opex_pt_total
        vrt = [total, -opex_vehicles_total, -opex_heavyvehicles_pb, -opex_pt_total, 0]

        fig = go.Figure()
        fig.add_waterfall(
            base=0,
            orientation="v",
            x=hrz,
            y=vrt,
            connector={"line": {"width": 0}},
            decreasing={"marker": {"color": "#ef553b"}},
            increasing={"marker": {"color": "#00cc96"}},
            totals={"marker": {"color": "#636efa"}},
            text=[str(round(np.absolute(i), 2)) + "SEK" for i in vrt],
            textposition="auto"
        )
        fig.update_layout(dict(
            margin=go.layout.Margin(
                l=40,
                r=20,
                b=5,
                t=60
            ),
            autosize=True,
            title_text="Per capita OPEX expenditure in {} (SEK)".format(mun),
            title_font=dict(size=18, color="darkred")
        ))
        return [fig]

@app.callback(
    Output('tabs-example-content-1', 'children'),
    [Input('tabs-example-1', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        collapse_2()
    if tab == "tab-2":
        collapse_3()

@app.callback(
    [
        Output("collapse-1", "is_open"),
        Output("clothing-collapse", "is_open"),
        Output("housing-collapse", "is_open"),
        Output("transport-collapse", "is_open"),
        Output("air-collapse", "is_open"),
        Output("recreation-collapse", "is_open"),
        Output("rh-collapse", "is_open"),
        Output("vehicles-collapse", "is_open"),
        Output("electricity-collapse", "is_open"),
        Output("dh-collapse", "is_open"),
        Output("hh-collapse", "is_open"),
    ],
    [
        Input("food-collapse", "n_clicks"),
        Input("clothing-collapse-button", "n_clicks"),
        Input("housing-collapse-button", "n_clicks"),
        Input("transport-collapse-button", "n_clicks"),
        Input("air-collapse-button", "n_clicks"),
        Input("recreation-collapse-button", "n_clicks"),
        Input("rh-collapse-button", "n_clicks"),
        Input("vehicles-collapse-button", "n_clicks"),
        Input("electricity-collapse-button", "n_clicks"),
        Input("dh-collapse-button", "n_clicks"),
        Input("hh-collapse-button", "n_clicks")
    ],
    [State("collapse-1", "is_open"),
    State("clothing-collapse", "is_open"),
    State("housing-collapse", "is_open"),
    State("transport-collapse", "is_open"),
    State("air-collapse", "is_open"),
    State("recreation-collapse", "is_open"),
    State("rh-collapse", "is_open"),
    State("vehicles-collapse", "is_open"),
    State("electricity-collapse", "is_open"),
    State("dh-collapse", "is_open"),
    State("hh-collapse", "is_open"),
    ]
)
def cbe_toggle_collapses(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11):
    ctx = dash.callback_context

    button_id=ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "food-collapse":
        if b1:
            return [not is_open1, False, False, False, False, False, False, False, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "clothing-collapse-button":
        if b2:
            return [False, not is_open2, False, False, False, False, False, False, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "housing-collapse-button":
        if b3:
            return [False, False, not is_open3, False, False, False, False, False, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "transport-collapse-button":
        if b4:
            return [False, False, False, not is_open4, False, False, False, False, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "air-collapse-button":
        if b5:
            return [False, False, False, False, not is_open5, False, False, False, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "recreation-collapse-button":
        if b6:
            return [False, False, False, False, False, not is_open6, False, False, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "rh-collapse-button":
        if b7:
            return [False, False, False, False, False, False, not is_open7, False, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "vehicles-collapse-button":
        if b8:
            return [False, False, False, False, False, False, False, not is_open8, False, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "electricity-collapse-button":
        if b9:
            return [False, False, False, False, False, False, False, False, not is_open9, False, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "dh-collapse-button":
        if b10:
            return [False, False, False, False, False, False, False, False, False, not is_open10, False]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]
    if button_id == "hh-collapse-button":
        if b11:
            return [False, False, False, False, False, False, False, False, False, False, not is_open11]
        return [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9, is_open10, is_open11]

@app.callback(
    [
        Output("transport-service-collapse", "is_open"),
        Output("air-transport-collapse", "is_open"),
        Output("vehicles-cars-collapse", "is_open"),
        Output("el-collapse", "is_open"),
        Output("house-heating-collapse", "is_open"),
        Output("heavy-collapse", "is_open")
    ],
    [
        Input("transport-service-collapse-button", "n_clicks"),
        Input("air-transport-collapse-button", "n_clicks"),
        Input("vehicles-cars-collapse-button", "n_clicks"),
        Input("el-collapse-button", "n_clicks"),
        Input("house-heating-collapse-button", "n_clicks"),
        Input("heavy-collapse-button", "n_clicks")
    ],
    [
        State("transport-service-collapse", "is_open"),
        State("air-transport-collapse", "is_open"),
        State("vehicles-cars-collapse", "is_open"),
        State("el-collapse", "is_open"),
        State("house-heating-collapse", "is_open"),
        State("heavy-collapse", "is_open")
    ]
)
def tbe_toggle_collapses(b1, b2, b3, b4, b5, b6, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6):
    ctx = dash.callback_context

    button_id=ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "transport-service-collapse-button":
        if b1:
            return not is_open1, False, False, False, False, False
        return is_open1, is_open2, is_open3, is_open4, is_open5, is_open6
    if button_id == "air-transport-collapse-button":
        if b2:
            return False, not is_open2, False, False, False, False
        return is_open1, is_open2, is_open3, is_open4, is_open5, is_open6
    if button_id == "vehicles-cars-collapse-button":
        if b3:
            return False, False, not is_open3, False, False, False
        return is_open1, is_open2, is_open3, is_open4, is_open5, is_open6
    if button_id == "el-collapse-button":
        if b4:
            return False, False, False, not is_open4, False, False
        return is_open1, is_open2, is_open3, is_open4, is_open5, is_open6
    if button_id == "house-heating-collapse-button":
        if b5:
            return False, False, False, False, not is_open5, False
        return is_open1, is_open2, is_open3, is_open4, is_open5, is_open6
    if button_id == "heavy-collapse-button":
        if b6:
            return False, False, False, False, False, not is_open6
        return is_open1, is_open2, is_open3, is_open4, is_open5, is_open6

@app.callback(
    Output("collapse-0", "is_open"),
    [Input("collapse-button-1", "n_clicks")],
    [State("collapse-0", "is_open")],
)
def toggle_collapse_2(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-2", "is_open"),
    [Input("collapse-button-2", "n_clicks")],
    [State("collapse-2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("initial-modal", "is_open"),
    [Input("initial-modal-closer", "n_clicks")],
    [State("initial-modal", "is_open")],
)
def close_modal(n, is_open):
    if n:
        return not is_open

@app.callback(
    Output("glossary-modal", "is_open"),
    [Input("glossary-button", "n_clicks")],
    [State("glossary-modal", "is_open")]
)
def glossary_modal(n, is_open):
    if n:
        return not is_open

@app.callback(
    Output("methodology-modal", "is_open"),
    [Input("methodology-button", "n_clicks")],
    [State("methodology-modal", "is_open")]
)
def methodology_modal(n, is_open):
    if n:
        return not is_open

@app.callback(
    Output("info-modal", "is_open"),
    [Input("modal-opener", "n_clicks"), Input("modal-closer", "n_clicks")],
    [State("info-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("municipality-dropdown", "options"),
    [Input("region-dropdown", "value")],
)
def dropdowns_interact(value):
    if value is None:
        return list(municipalities)
    elif value == "Gotlands län":
        return ["Gotland"]
    else:
        return list(regions_län.loc[value, "Municipality"])

app.layout = html.Div([
    build_banner(), collapse(),
    dcc.Tabs(id='tabs-example-1', value = "tab-1", children=[
    dcc.Tab(id="tab-1", label="Consumption-based emissions (households only)", value="tab-1", children=[collapse_2()]),
    dcc.Tab(id="tab-2", label="Territorial emissions", value="tab-2", children=[collapse_3()])]),
    html.Div(id='tabs-example-content-1')
])

#if __name__ == '__main__':
#   app.run_server(debug=False, port=8080, host='0.0.0.0')

if __name__ == '__main__':
    app.run_server(debug=False)
