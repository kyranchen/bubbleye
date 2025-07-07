import streamlit as st
import moloco_simulator

st.set_page_config(layout="wide", page_title="Bubbleye Ad Manager (Mock)")

st.title("Bubbleye Ad Manager - Mock Application")
st.subheader("Simulating Moloco API Interactions")

st.write("---")

st.header("Moloco Campaigns Overview")

# Simulate fetching campaigns
campaigns_response = moloco_simulator.simulate_get_campaigns()

if "data" in campaigns_response:
    st.success("Successfully fetched mock campaigns!")
    campaigns = campaigns_response["data"]

    for campaign in campaigns:
        st.markdown(f"**Campaign Name:** {campaign['name']} (ID: `{campaign['id']}`)")
        st.write(f"**Status:** {campaign['status']}")
        st.write(f"**Type:** {campaign['type']}")
        st.write(f"**Creative Groups Attached:** {len(campaign['creative_group_ids'])}")
        
        # Display attached creative groups
        if campaign['creative_group_ids']:
            with st.expander(f"View Creative Groups for {campaign['name']}"):
                for cg_id in campaign['creative_group_ids']:
                    if cg_id in moloco_simulator._MOLOCO_CREATIVE_GROUPS:
                        cg_name = moloco_simulator._MOLOCO_CREATIVE_GROUPS[cg_id]['name']
                        st.write(f"- `{cg_id}`: {cg_name}")
                    else:
                        st.write(f"- `{cg_id}` (Not found in data store - might be mock placeholder)")
        st.markdown("---")

else:
    st.error(f"Error fetching campaigns: {campaigns_response.get('error', 'Unknown error')}")

st.write("---")

st.header("Simulate New Creative Concept Upload")

# Simulate uploading a portrait and landscape video for a new concept
if st.button("Simulate New Creative Concept"):
    st.info("Simulating upload of portrait video...")
    portrait_asset_response = moloco_simulator.simulate_upload_asset("new_portrait_video.mp4")
    portrait_asset_id = portrait_asset_response["data"]["id"]
    st.success(f"Portrait video uploaded. Asset ID: `{portrait_asset_id}`")

    st.info("Simulating upload of landscape video...")
    landscape_asset_response = moloco_simulator.simulate_upload_asset("new_landscape_video.mp4")
    landscape_asset_id = landscape_asset_response["data"]["id"]
    st.success(f"Landscape video uploaded. Asset ID: `{landscape_asset_id}`")

    st.info("Simulating creative creation for portrait video...")
    portrait_creative_response = moloco_simulator.simulate_create_creative(
        name="New Portrait Creative",
        creative_type="VIDEO",
        asset_id=portrait_asset_id,
        video_property={"auto_endcard": True}
    )
    portrait_creative_id = portrait_creative_response["data"]["id"]
    st.success(f"Portrait creative created. Creative ID: `{portrait_creative_id}`")

    st.info("Simulating creative creation for landscape video...")
    landscape_creative_response = moloco_simulator.simulate_create_creative(
        name="New Landscape Creative",
        creative_type="VIDEO",
        asset_id=landscape_asset_id,
        video_property={"auto_endcard": True}
    )
    landscape_creative_id = landscape_creative_response["data"]["id"]
    st.success(f"Landscape creative created. Creative ID: `{landscape_creative_id}`")

    st.info("Simulating creative group creation...")
    new_creative_group_name = f"New_Concept_CG_{moloco_simulator._generate_id()}"
    creative_group_response = moloco_simulator.simulate_create_creative_group(
        name=new_creative_group_name,
        creative_ids=[portrait_creative_id, landscape_creative_id]
    )
    if "data" in creative_group_response:
        new_cg_id = creative_group_response["data"]["id"]
        st.success(f"Creative group '{new_cg_id}' created successfully!")
        st.session_state["last_created_cg_id"] = new_cg_id # Store for later use in session state
    else:
        st.error(f"Failed to create creative group: {creative_group_response.get('error', 'Unknown error')}")


st.write("---")

st.header("Attach to Creative Testing Campaign")

if "last_created_cg_id" in st.session_state:
    st.write(f"Newly created Creative Group to attach: `{st.session_state['last_created_cg_id']}`")
    if st.button(f"Attach {st.session_state['last_created_cg_id']} to creative_testing_campaign"):
        attach_response = moloco_simulator.simulate_add_creative_groups_to_campaign(
            campaign_id="creative_testing_campaign",
            new_creative_group_ids=[st.session_state["last_created_cg_id"]]
        )
        if "message" in attach_response:
            st.success(attach_response["message"])
            del st.session_state["last_created_cg_id"] # Clear it after attaching
        else:
            st.error(f"Failed to attach: {attach_response.get('error', 'Unknown error')}")
else:
    st.info("Simulate a new creative concept first to get a Creative Group to attach.")

st.write("---")

st.header("Manage Creative Testing Campaign Status")
test_campaign = moloco_simulator._MOLOCO_CAMPAIGNS.get("creative_testing_campaign")
if test_campaign:
    st.write(f"Current Status of 'creative_testing_campaign': **{test_campaign['status']}**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Testing Campaign"):
            status_response = moloco_simulator.simulate_update_campaign_status("creative_testing_campaign", "RUNNING")
            if "data" in status_response:
                st.success(f"Campaign status updated to: {status_response['data']['status']}")
            else:
                st.error(f"Failed to update status: {status_response.get('error', 'Unknown error')}")
    with col2:
        if st.button("Pause Testing Campaign"):
            status_response = moloco_simulator.simulate_update_campaign_status("creative_testing_campaign", "PAUSED")
            if "data" in status_response:
                st.success(f"Campaign status updated to: {status_response['data']['status']}")
            else:
                st.error(f"Failed to update status: {status_response.get('error', 'Unknown error')}")

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

st.header("Champions Waiting Queue")
queue_status = moloco_simulator.simulate_get_champion_queue_status()
if queue_status and queue_status["data"]:
    st.write("Current Champions in Queue:")
    for champion_id in queue_status["data"]:
        st.write(f"- `{champion_id}`")
else:
    st.info("No champion concepts currently in the waiting queue.")


st.write("---")

st.header("Manage Regular Campaigns")
regular_campaigns = [moloco_simulator._MOLOCO_CAMPAIGNS["regular_campaign_a"], moloco_simulator._MOLOCO_CAMPAIGNS["regular_campaign_b"]]

for reg_camp in regular_campaigns:
    st.subheader(f"Campaign: {reg_camp['name']}")
    st.write(f"Current Status: {reg_camp['status']}")
    st.write(f"Creative Groups: {reg_camp['creative_group_ids']}")

    if st.button(f"Replace Worst in {reg_camp['name']}", key=f"replace_{reg_camp['id']}"):
        replace_response = moloco_simulator.simulate_replace_worst_creative_in_regular_campaign(reg_camp['id'])
        if "message" in replace_response:
            st.success(replace_response["message"])
        else:
            st.error(f"Failed to replace: {replace_response.get('error', 'Unknown error')}")

st.write("---")

st.header("Refresh Data")
if st.button("Refresh All Data"):
    st.experimental_rerun() # Rerun the app to show updated state