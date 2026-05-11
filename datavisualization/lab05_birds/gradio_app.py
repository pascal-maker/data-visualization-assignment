import gradio as gr#importing gradio
import httpx#importing httpx
import pandas as pd#importing pandas

BASE_URL = "http://127.0.0.1:8000"#setting the base url

conservation_statuses = [
    "Least Concern",
    "Near Threatened",
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
    "Extinct in the Wild",
    "Extinct"
]

families = [
    "Passeridae",
    "Muscicapidae",
    "Tytonidae",
    "Ciconiidae",
    "Accipitridae",
    "Anatidae",
    "Corvidae"
]

def get_species():#function to get the species
    response = httpx.get(f"{BASE_URL}/species/")#getting the species from the api
    response.raise_for_status()#raising http exception if the response is not ok
    return pd.DataFrame(response.json())#returning the species as a pandas dataframe

def add_species(name, scientific_name, family, conservation_status, wingspan_cm):#function to add a species
    payload = {
        "name": name,
        "scientific_name": scientific_name,
        "family": family,
        "conservation_status": conservation_status,
        "wingspan_cm": wingspan_cm
    }
    response = httpx.post(f"{BASE_URL}/species/", json=payload)#posting the species to the api
    response.raise_for_status()#raising http exception if the response is not ok
    return (
        "Species added successfully",
        get_species()
    )

def get_species_choices():#function to get the species choices
    response = httpx.get(f"{BASE_URL}/species/")#getting the species from the api
    response.raise_for_status()#raising http exception if the response is not ok
    species_list = response.json()
    return [f"{species['name']} ({species['scientific_name']})", species["id"] for species in species_list]#

def get_birds():#function to get the birds
    response = httpx.get(f"{BASE_URL}/birds/")#getting the birds from the api
    response.raise_for_status()#raising http exception if the response is not ok
    return pd.DataFrame(response.json())#returning the birds as a pandas dataframe

def add_bird(nickname, ring_code, age, species_id):
    payload = {
        "nickname": nickname,
        "ring_code": ring_code,
        "age": age,
        "species_id": species_id
    }
    response = httpx.post(f"{BASE_URL}/birds/", json=payload)#posting the bird to the api
    response.raise_for_status()#raising http exception if the response is not ok
    return (
        "Bird added successfully",
        get_birds()
    )

def get_bird_choices():#function to get the bird choices
    response = httpx.get(f"{BASE_URL}/birds/")#getting the birds from the api
    response.raise_for_status()#raising http exception if the response is not ok
    birds = response.json()
    return [(f"{bird['nickname']} ({bird['ring_code']})", bird["id"]) for bird in birds]

def get_sightings():#function to get the sightings
    response = httpx.get(f"{BASE_URL}/birdspotting/")#getting the sightings from the api
    response.raise_for_status()#raising http exception if the response is not ok
    return pd.DataFrame(response.json())#returning the sightings as a pandas dataframe

def add_sighting(bird_id, spotted_at, location, observer_name, notes):#function to add a sighting
    payload = {
        "bird_id": bird_id,#
        "spotted_at": spotted_at,#
        "location": location,#
        "observer_name": observer_name,#
        "notes": notes#
    }
    response = httpx.post(f"{BASE_URL}/birdspotting/", json=payload)#posting the sighting to the api
    response.raise_for_status()#raising http exception if the response is not ok
    return "Sighting added successfully", get_sightings()#returning the sightings as a pandas dataframe

with gr.Blocks() as demo:
    gr.Markdown("# Bird API integration")#setting the title of the app
    gr.Markdown("Use this interface to manage species, birds, and sightings.")#setting the description of the app

    with gr.Tab("Species"):
        gr.Markdown("## Species")#setting the title of the species tab
        gr.Markdown("View all species and add a new species.")#setting the description of the species tab

        s_name = gr.Textbox(label="Name")#setting the name of the species
        s_scientific_name = gr.Textbox(label="Scientific name")#setting the scientific name of the species
        s_family = gr.Dropdown(
            choices=families,#setting the family of the species
            label="Family",#setting the label of the family
            allow_custom_value=True,#allowing custom values for the family
            filterable=True#filtering the family
        )
        s_status = gr.Dropdown(#setting the conservation status of the species
            choices=conservation_statuses,#setting the conservation status of the species
            label="Conservation status"#setting the label of the conservation status
        )
        s_wingspan = gr.Slider(#setting the wingspan of the species
            minimum=1,#setting the minimum value of the wingspan
            maximum=300,#setting the maximum value of the wingspan
            step=1,#setting the step value of the wingspan
            value=20,#setting the value of the wingspan
            label="Wingspan (cm)"#setting the label of the wingspan
        )

        s_add_btn = gr.Button("Add species")#setting the add species button
        s_refresh_btn = gr.Button("Refresh species")#setting the refresh species button
        s_message = gr.Textbox(label="Message")#setting the message text box
        s_table = gr.DataFrame(label="Species data")#setting the species data table

        s_add_btn.click(
            fn=add_species,#adding the species to the api
            inputs=[s_name, s_scientific_name, s_family, s_status, s_wingspan],#inputs of the add species function
            outputs=[s_message, s_table]#outputs of the add species function
        )

        s_refresh_btn.click(
            fn=get_species,#getting the species from the api
            inputs=[],#inputs of the get species function
            outputs=s_table#outputs of the get species function
        )

    with gr.Tab("Birds"):#setting the birds tab
        gr.Markdown("## Birds")#setting the title of the birds tab
        gr.Markdown("View all birds and add a new bird linked to a species.")#setting the description of the birds tab

        b_nickname = gr.Textbox(label="Nickname")#setting the nickname of the bird
        b_ring_code = gr.Textbox(label="Ring code")#setting the ring code of the bird
        b_age = gr.Number(label="Age", minimum=0, value=1)#setting the age of the bird
        b_species = gr.Dropdown(
            choices=get_species_choices(),#setting the species of the bird
            label="Species"#setting the label of the species
        )

        b_add_btn = gr.Button("Add bird")#setting the add bird button
        b_refresh_btn = gr.Button("Refresh birds")#setting the refresh birds button
        b_message = gr.Textbox(label="Message")#setting the message text box
        b_table = gr.DataFrame(label="Bird data")#setting the bird data table

        b_add_btn.click(
            fn=add_bird,#adding the bird to the api
            inputs=[b_nickname, b_ring_code, b_age, b_species],#inputs of the add bird function
            outputs=[b_message, b_table]#outputs of the add bird function
        )

        b_refresh_btn.click(#refreshing the birds and the species choices
            fn=lambda: [get_birds(), gr.update(choices=get_species_choices())],#getting the birds and the species choices
            inputs=[],#inputs of the refresh birds function
            outputs=[b_table, b_species]#outputs of the refresh birds function
        )

    with gr.Tab("Sightings"):#setting the sightings tab
        gr.Markdown("## Sightings")#setting the title of the sightings tab
        gr.Markdown("View all sightings and add a new sighting linked to a bird.")#setting the description of the sightings tab

        bs_bird = gr.Dropdown(
            choices=get_bird_choices(),#setting the bird choices
            label="Bird"#setting the label of the bird
        )
        bs_spotted_at = gr.Textbox(
            label="Spotted at",#setting the label of the spotted at
            value="2026-03-30T14:00:00"#setting the default value of the spotted at
        )
        bs_location = gr.Textbox(label="Location")#setting the label of the location
        bs_observer = gr.Textbox(label="Observer name")#setting the label of the observer name
        bs_notes = gr.Textbox(label="Notes")#setting the label of the notes

        bs_add_btn = gr.Button("Add sighting")#setting the add sighting button
        bs_refresh_btn = gr.Button("Refresh sightings")#setting the refresh sightings button
        bs_message = gr.Textbox(label="Message")#setting the message text box
        bs_table = gr.DataFrame(label="Sightings data")#setting the sightings data table

        bs_add_btn.click(
            fn=add_sighting,#adding the sighting to the api
            inputs=[bs_bird, bs_spotted_at, bs_location, bs_observer, bs_notes],#inputs of the add sighting function
            outputs=[bs_message, bs_table]#outputs of the add sighting function
        )

        bs_refresh_btn.click(
            fn=lambda: [gr.update(choices=get_bird_choices()), get_sightings()],#getting the birds and the sightings
            inputs=[],
            outputs=[bs_bird, bs_table]
        )

demo.launch()#launching the app