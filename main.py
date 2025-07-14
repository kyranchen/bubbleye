import streamlit as st
import moloco_simulator
import env_variables as env
import requests

st.set_page_config(layout="wide", page_title="Bubbleye Ad Manager (Mock)")

st.title("Bubbleye Ad Manager - Mock Application")
st.subheader("Simulating Moloco API Interactions")

st.write("---")

st.header("Moloco Campaigns Overview")

# Call API (List up Campaigns)
# This is a mock API call to simulate fetching active campaigns
# Example of calling the local Flask API endpoint from moloco_simulator
# (Assuming your Flask app is running locally on port 5000)

url = "http://localhost:8080/cm/v1/campaigns"
params = {
    "ad_account_id": env.ad_account_id,
    "product_id": env.product_id,
    "states": "ACTIVE",
    "fetch_option": "UNKNOWN_FETCH_OPTION"
}
headers = {"accept": "application/json"}

response = requests.get(url, headers=headers, params=params)
try:
    campaigns_response = response.json()
except Exception as e:
    st.error(f"Failed to decode JSON from API. Status code: {response.status_code}\nResponse text: {response.text}")

if "data" in campaigns_response:
    st.success("Successfully fetched mock campaigns!")
    campaigns = campaigns_response["data"]

    for campaign in campaigns:
        st.markdown(f"**Campaign Name:** {campaign['description']} (ID: `{campaign['title']}`)")
        st.write(f"**Status:** {campaign['status']}")
        st.write(f"**Type:** {campaign['type']}")
        st.write(f"**Creative Groups Attached:** {len(campaign['ad_group_ids'])}")
        cg_key = f"creative_groups_{campaign['campaign_id']}"
        if cg_key not in st.session_state:
            st.session_state[cg_key] = list(campaign['ad_group_ids'])
        # Always display the latest creative groups from session_state
        st.write(f"Creative Groups: {st.session_state[cg_key]}")
        if st.button(f"Replace Worst in {campaign['description']}", key=f"replace_{campaign['campaign_id']}"):
            replace_response = moloco_simulator.simulate_replace_worst_creative_in_regular_campaign(campaign['campaign_id'])
            if "message" in replace_response:
                st.success(replace_response["message"])
                # Update session_state with the new creative group list
                st.session_state[cg_key] = st.session_state[cg_key] + [replace_response["new_champion_id"]]
                if replace_response["replaced_cg_id"]:
                    st.session_state[cg_key].remove(replace_response["replaced_cg_id"])
                # Display the updated creative groups immediately
                st.write(f"Updated Creative Groups: {st.session_state[cg_key]}")
            else:
                st.error(f"Failed to replace: {replace_response.get('error', 'Unknown error')}")

        # Display attached creative groups
        params = {
            "date_range": {
                "start": "20250601",
                "end": "20250701"
            },
            "ad_account_id": env.ad_account_id,
            "dimensions": [
                "AD_GROUP_ID",
                "CAMPAIGN_ID"
            ],
            "metrics": [
                "INSTALLS"
            ],
            "dimension_filters": [
                {
                "dimension": "CAMPAIGN_ID",
                "operator": "IN",
                "values": [
                    "campaign_id_123"
                ]
                }
            ],
            "order_by_filters": [
                {
                "dimension": "CAMPAIGN_ID",
                "metric": "INSTALLS",
                "is_descending": True
                }
            ]
        }
        # if campaign['creative_group_ids']:
        #     with st.expander(f"View Creative Groups for {campaign['title']}"):
        #         for cg_id in campaign['creative_group_ids']:
        #             if cg_id in moloco_simulator._MOLOCO_CREATIVE_GROUPS:
        #                 cg_name = moloco_simulator._MOLOCO_CREATIVE_GROUPS[cg_id]['name']
        #                 st.write(f"- `{cg_id}`: {cg_name}")
        #             else:
        #                 st.write(f"- `{cg_id}` (Not found in data store - might be mock placeholder)")
        st.markdown("---")
else:
    st.error(f"Error fetching campaigns: {campaigns_response.get('error', 'Unknown error')}")
st.write("---")

st.header("Champions Waiting Queue")
queue_status = moloco_simulator.simulate_get_champion_queue_status()
if queue_status and queue_status["data"]:
    st.write("Current Champions in Queue:")
    for champion_id in queue_status["data"]:
        st.write(f"- `{champion_id}`")
else:
    st.info("No champion concepts currently in the waiting queue.")

st.write("---")
st.header("New Creative Concept Upload")

# Simulate uploading a portrait and landscape video for a new concept
uploaded_file1 = st.file_uploader("Choose a file", type=["txt", "png", "jpg", "jpeg", "pdf", "mp3", "mp4"])
uploaded_file2 = st.file_uploader("Choose a second file", type=["txt", "png", "jpg", "jpeg", "pdf", "mp3", "mp4"])
if uploaded_file1 is not None and uploaded_file2 is not None:
    if st.button("Upload New Creative Concept"):
        st.info("Simulating upload of portrait video...")
        url = "http://localhost:8080/cm/v1/creatives"
        params = {
            "ad_account_id": env.ad_account_id,
            "product_id": env.product_id,
            "title": uploaded_file1.name,
            "type": "VIDEO",
            "ad_type": "PORTRAIT"  # Specify ad type for portrait video
        }
        portrait_asset_response = requests.post(url, headers=headers, params=params)
        portrait_asset_response_json = portrait_asset_response.json()
        if "error" in portrait_asset_response_json:
            st.error(f"Failed to upload portrait video: {portrait_asset_response_json['error']}")
        else:
            portrait_creative_id = portrait_asset_response_json["data"]["id"]
            st.success(f"Portrait video uploaded. Creative ID: `{portrait_creative_id}`")

        st.info("Simulating upload of landscape video...")
        params = {
            "ad_account_id": env.ad_account_id,
            "product_id": env.product_id,
            "title": uploaded_file2.name,
            "type": "VIDEO", 
            "ad_type": "LANDSCAPE"  # Specify ad type for landscape video
        }
        landscape_asset_response = requests.post(url, headers=headers, params=params)
        landscape_asset_response_json = landscape_asset_response.json()
        if "error" in landscape_asset_response_json:
            st.error(f"Failed to upload landscape video: {landscape_asset_response_json['error']}")
        else:
            landscape_creative_id = landscape_asset_response_json["data"]["id"]
            st.success(f"Landscape video uploaded. Creative ID: `{landscape_creative_id}`")

st.write("---")
st.header("Create New Creative Group")
# Fetch all portrait and landscape creatives
url = "http://localhost:8080/cm/v1/creatives/PORTRAIT"
params = {"ad_type": "PORTRAIT"}
portrait_response = requests.get(url, headers=headers, params=params)
portrait_creatives = portrait_response.json().get("data", [])
portrait_creative_id = st.selectbox(
    "Select Portrait Creative",
    options=[c["id"] for c in portrait_creatives],
    format_func=lambda cid: next((c["title"] for c in portrait_creatives if c["id"] == cid), cid),
    key="portrait_creative_select"
)
url = "http://localhost:8080/cm/v1/creatives/LANDSCAPE"
params = {"ad_type": "LANDSCAPE"}
landscape_response = requests.get(url, headers=headers, params=params)
landscape_creatives = landscape_response.json().get("data", [])
landscape_creative_id = st.selectbox(
    "Select Landscape Creative",
    options=[c["id"] for c in landscape_creatives],
    format_func=lambda cid: next((c["title"] for c in landscape_creatives if c["id"] == cid), cid),
    key="landscape_creative_select"
)
creative_group_title = st.text_input("Creative Group Title", value="New Creative Group")
creative_group_description = st.text_area("Creative Group Description", value="Description of the new creative group")

# Maintain a list of the last two created creative group IDs in session state
if "last_created_cg_ids" not in st.session_state:
    st.session_state["last_created_cg_ids"] = []

if st.button("Upload Portrait and Landscape Creatives"):
    st.info("Simulating creative group creation...")
    new_creative_group_name = creative_group_title or "New Creative Group"
    new_creative_group_description = creative_group_description or "Description of the new creative group"
    url = "http://localhost:8080/cm/v1/creative_groups"
    params = {
        "title": new_creative_group_name,
        "description": new_creative_group_description,
        "creative_ids": [portrait_creative_id, landscape_creative_id]
    }
    creative_group_response = requests.post(url, headers=headers, json=params)
    creative_group_response_json = creative_group_response.json()
    if "data" in creative_group_response_json:
        new_cg_id = creative_group_response_json["data"]["id"]
        st.success(f"Creative group '{new_cg_id}' created successfully!")
        st.session_state["last_created_cg_ids"].append(new_cg_id)
    else:
        st.error(f"Failed to create creative group: {creative_group_response}")


st.write("---")

url = "http://localhost:8080/cm/v1/campaigns/creative_testing_campaign"
fetch_campaign_response = requests.get(url, headers=headers)
test_campaign = fetch_campaign_response.json().get("data", None)
if test_campaign:
    st.session_state["testing_campaign_ad_group_ids"] = test_campaign.get('ad_group_ids', [])

st.header("Attach Creatives to Testing Campaign")

if st.session_state["last_created_cg_ids"]:
    st.write("Newly created Creative Groups to attach:")
    for cg_id in st.session_state["last_created_cg_ids"]:
        st.write(f"- `{cg_id}`")
    if st.button(f"Attach {', '.join(st.session_state['last_created_cg_ids'])} to creative_testing_campaign"):
        print(st.session_state["last_created_cg_ids"])
        url = "http://localhost:8080/cm/v1/campaigns/creative_testing_campaign"
        params = {
            "creative_group_ids": st.session_state["last_created_cg_ids"],
            "ad_account_id": env.ad_account_id,
            "product_id": env.product_id
        }
        attach_response = requests.post(url, headers=headers, json=params)
        attach_response_json = attach_response.json()
        if "message" in attach_response_json:
            st.success(attach_response_json["message"])
            st.session_state["testing_campaign_ad_group_ids"].extend(st.session_state["last_created_cg_ids"])
            st.session_state["last_created_cg_ids"] = []  # Clear after attaching
        else:
            st.error(f"Failed to attach")
else:
    st.info("Simulate new creative concepts first to get Creative Groups to attach.")

st.write("---")

st.header("Manage Creative Testing Campaign")
# Simulate fetching the testing campaign
if test_campaign:
    st.write(f"Current Status of 'creative_testing_campaign': **{test_campaign['status']}**")
    st.write(f"**Testing Campaign ID:** `{test_campaign['campaign_id']}`")
    test_campaign_ad_group_ids = st.session_state.get("testing_campaign_ad_group_ids", [])

    for ad_group_id in test_campaign_ad_group_ids:
        url = "http://localhost:8080/cm/v1/ad_groups/" + ad_group_id
        ad_group_response = requests.get(url, headers=headers)
        ad_group_data = ad_group_response.json().get("data", {})
        if ad_group_data:
            with st.expander(f"Ad Group ID: `{ad_group_id}`", expanded=False):
                st.write(f"**Performance:** {ad_group_data.get('performance', {})}")
    
    if st.button("Start Testing Campaign"):
        url = "http://localhost:8080/cm/v1/campaigns/creative_testing_campaign"
        params = {"status": "RUNNING", "creative_group_ids": []}
        status_response = requests.post(url, headers=headers, json=params)
        status_response_json = status_response.json()
        if "message" in status_response_json:
            st.success(f"Campaign status updated to: RUNNING")
        else:
            st.error(f"Failed to update status")
    if st.button("Pause Testing Campaign"):
        moloco_simulator.simulate_campaign_performance("creative_testing_campaign")
        url = "http://localhost:8080/cm/v1/campaigns/creative_testing_campaign"
        params = {"status": "PAUSED", "creative_group_ids": []}
        status_response = requests.post(url, headers=headers, json=params)
        status_response_json = status_response.json()
        if "message" in status_response_json:
            st.success(f"Campaign status updated to: PAUSED")
        else:
            st.error(f"Failed to update status")

st.write("---")

st.header("Evaluate Testing Campaign & Champions")
if st.button("Evaluate Creative Testing Campaign"):
    eval_response = moloco_simulator.simulate_evaluate_testing_campaign("creative_testing_campaign")
    if "message" in eval_response:
        st.success(eval_response["message"])
        st.write(f"Champions Identified: {eval_response['champions_identified']}")
        st.write(f"Champions in Waiting Queue: {eval_response['queue_size']}")
    else:
        st.error(f"Evaluation failed: {eval_response.get('error', 'Unknown error')}")

st.write("---")


st.write("---")

st.header("Refresh Data")
if st.button("Refresh All Data"):
    st.experimental_rerun() # Rerun the app to show updated state