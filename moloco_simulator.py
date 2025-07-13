import uuid
import datetime
import random
import env_variables as env
from flask import Flask, jsonify, request
from dtos.campaign import Campaign
from dtos.ad_group import AdGroup
from dtos.creative_group import CreativeGroup
from dtos.creative import Creative

# --- In-memory Data Stores (Mock Moloco Database) ---
# Each dictionary stores entities by their unique ID.

_MOLOCO_CREATIVES = [] # Stores mock creative data
_MOLOCO_CREATIVE_GROUPS = [] # Stores mock creative group data
testing_campaign = Campaign(
    ad_account_id=env.ad_account_id,
    product_id=env.product_id,
    campaign_id="creative_testing_campaign",
    title="creative_testing_campaign",
    description="creative_testing_campaign",
    status="PAUSED", # Initial status as per requirements implicitly
    creative_group_ids=["good_creative_group"], # Initially includes the control group
    type="TESTING",
    createTime=datetime.datetime.now().isoformat(),
    lastModifiedTime=datetime.datetime.now().isoformat(),
    impressions_goal_per_cg=10000 # Specific for this testing campaign
)
regular_campaign_a = Campaign(
    ad_account_id=env.ad_account_id,
    product_id=env.product_id,
    campaign_id="regular_campaign_a",
    title="regular_campaign_a",
    description="Regular Campaign A",
    status="ACTIVE",
    creative_group_ids=[
        ""
    ], # Initially empty, or pre-filled with mock data
    type="REGULAR",
    createTime=datetime.datetime.now().isoformat(),
    lastModifiedTime=datetime.datetime.now().isoformat(),
)
regular_campaign_b = Campaign(
    ad_account_id=env.ad_account_id,
    product_id=env.product_id,
    campaign_id="regular_campaign_b",
    title="regular_campaign_b",
    description="Regular Campaign B",
    status="ACTIVE",
    creative_group_ids=[], # Initially empty, or pre-filled with mock data
    type="REGULAR",
    createTime=datetime.datetime.now().isoformat(),
    lastModifiedTime=datetime.datetime.now().isoformat(),
)
_MOLOCO_CAMPAIGNS = [
    testing_campaign,
    regular_campaign_a,
    regular_campaign_b
]
# Stores champion creative group IDs in a waiting line
champion_ad1 = AdGroup(
    ad_group_id="champion_cg_1",
    campaign_id="creative_testing_campaign",
    creative_group_ids=["champion_cg_1"],
    performance={"impressions": 1000, "conversions": 123}
)
champion_ad2 = AdGroup(
    ad_group_id="champion_cg_2",
    campaign_id="creative_testing_campaign",
    creative_group_ids=["champion_cg_2"], 
    performance={"impressions": 1000, "conversions": 150}
)
champion_ad3 = AdGroup(
    ad_group_id="champion_cg_3",
    campaign_id="creative_testing_campaign",
    creative_group_ids=["champion_cg_3"], 
    performance={"impressions": 1000, "conversions": 200}
)
_MOLOCO_CHAMPION_CONCEPTS_QUEUE = [
    champion_ad1, champion_ad2, champion_ad3
] 

# Pre-populate the "good_creative_group" as it's a control group

app = Flask(__name__)
# --- Helper Function for ID Generation ---
def _generate_id(prefix="id"):
    """Generates a unique ID with a given prefix."""
    return f"{prefix}_{str(uuid.uuid4()).replace('-', '_')[:8]}"

# --- Simulation Functions (Mock Moloco API Endpoints) ---
@app.route('/cm/v1/creatives', methods=['POST'])
def upload_creative():
    """
    Simulates the Moloco API call to upload an asset.
    Returns a mock response dictionary.
    """
    ad_account_id = request.args.get("ad_account_id")
    product_id = request.args.get("product_id")
    creative_id = _generate_id("creative")
    title = request.args.get("title", "New Creative")
    type = request.args.get("type")
    ad_type = request.args.get("ad_type")
    upload_time = random.randint(2, 10) # Simulate varying upload times
    now = datetime.datetime.now().isoformat()
    creative = Creative(
        id=creative_id, 
        ad_account_id=ad_account_id,
        product_id=product_id,
        title=title, 
        type=type,
        ad_type=ad_type,
        video_property={"auto_endcard": True}, # Assume video property for simplicity
        createTime=now,
        lastModifiedTime=now
    )
    _MOLOCO_CREATIVES.append(creative)
    return jsonify({"data": {"id": creative_id, "status": "uploaded", "upload_time_seconds": upload_time}})

@app.route('/cm/v1/creatives/<ad_type>', methods=['GET'])
def get_creative_by_ad_type(ad_type):
    """
    Simulates the Moloco API call to retrieve a creative by its ad_type.
    Returns a mock response dictionary.
    """
    result = []
    for creative in _MOLOCO_CREATIVES:
        if creative.ad_type == ad_type:
            result.append(creative.to_dict())
    if result:
        return jsonify({"data": result})
    return jsonify({"error": f"No creatives found for ad_type '{ad_type}'."})

@app.route('/cm/v1/creative_groups', methods=['POST'])
def create_creative_group():
    """
    Simulates the Moloco API call to create a creative group.
    Returns a mock response dictionary.
    """
    creative_group_id = _generate_id("cg")
    creative_ids = request.args.getlist("creative_ids")
    creative_group = CreativeGroup(
        id=creative_group_id,
        title=request.args.get("title", "New Creative Group"),
        description=request.args.get("description", "No description provided"),
        creative_ids=creative_ids,
        status="ACTIVE",
        createTime=datetime.datetime.now().isoformat(),
        lastModifiedTime=datetime.datetime.now().isoformat()
    )
    _MOLOCO_CREATIVE_GROUPS.append(creative_group)
    return jsonify({"data": {"id": creative_group.id, "creatived_ids": creative_ids, "status": "ACTIVE"}})


@app.route('/cm/v1/campaigns', methods=['GET'])
def api_get_campaigns():
    """
    API endpoint to retrieve all campaign data.
    Supports Moloco-like query parameters: ad_account_id, product_id, states, fetch_option.
    """
    # For simulation, ignore query params but accept them for compatibility
    ad_account_id = request.args.get('ad_account_id')
    product_id = request.args.get('product_id')
    states = request.args.get('states')
    fetch_option = request.args.get('fetch_option')
    # Filter campaigns based on query params (if provided)
    campaign_list = []
    for c in _MOLOCO_CAMPAIGNS:
        if states and c.status != states:
            continue
        if ad_account_id and c.ad_account_id != ad_account_id:
            continue
        if product_id and c.product_id != product_id:
            continue
        campaign_list.append(c.to_dict() if hasattr(c, "to_dict") else c.__dict__)
    return jsonify({"data": campaign_list})

def simulate_add_creative_groups_to_campaign(campaign_id: str, new_creative_group_ids: list):
    """
    Simulates attaching creative groups to a campaign.
    """
    if campaign_id not in _MOLOCO_CAMPAIGNS:
        return {"error": f"Campaign '{campaign_id}' not found."}

    campaign = _MOLOCO_CAMPAIGNS[campaign_id]
    for cg_id in new_creative_group_ids:
        if cg_id not in _MOLOCO_CREATIVE_GROUPS:
            return {"error": f"Creative Group '{cg_id}' not found."}
        if cg_id not in campaign["creative_group_ids"]: # Avoid duplicates
            campaign["creative_group_ids"].append(cg_id)
    campaign["lastModifiedTime"] = datetime.datetime.now().isoformat()
    return {"message": "Creative groups attached successfully."}


def simulate_update_campaign_status(campaign_id: str, status: str):
    """
    Simulates updating a campaign's status (e.g., RUNNING, PAUSED).
    """
    if campaign_id not in _MOLOCO_CAMPAIGNS:
        return {"error": f"Campaign '{campaign_id}' not found."}
    if status not in ["RUNNING", "PAUSED"]:
        return {"error": "Invalid status. Must be 'RUNNING' or 'PAUSED'."}

    campaign = _MOLOCO_CAMPAIGNS[campaign_id]
    campaign["status"] = status
    campaign["lastModifiedTime"] = datetime.datetime.now().isoformat()

    return {"data": {"id": campaign_id, "status": status}}

def simulate_get_campaign_performance(campaign_id: str):
    """
    Simulates retrieving performance data for a campaign.
    For the testing campaign, it simulates impressions reaching the goal and random conversions.
    For regular campaigns, it simulates ongoing performance.
    """
    if campaign_id not in _MOLOCO_CAMPAIGNS:
        return {"error": f"Campaign '{campaign_id}' not found."}

    campaign = _MOLOCO_CAMPAIGNS[campaign_id]
    performance_data = {}

    for cg_id in campaign["creative_group_ids"]:
        if cg_id in _MOLOCO_CREATIVE_GROUPS:
            cg = _MOLOCO_CREATIVE_GROUPS[cg_id]
            if campaign["type"] == "TESTING" and campaign["status"] == "RUNNING":
                # Simulate reaching 10,000 impressions for testing campaign if running
                cg["performance"]["impressions"] = campaign["impressions_goal_per_cg"]
                # Simulate conversions based on impressions, with some randomness
                cg["performance"]["conversions"] = int(cg["performance"]["impressions"] * random.uniform(0.005, 0.015))
            elif campaign["type"] == "REGULAR" and campaign["status"] == "RUNNING":
                 # Simulate ongoing performance for regular campaigns
                cg["performance"]["impressions"] += random.randint(1000, 5000)
                cg["performance"]["conversions"] += random.randint(10, 50)

            performance_data[cg_id] = {
                "impressions": cg["performance"]["impressions"],
                "conversions": cg["performance"]["conversions"],
            }
    return {"data": performance_data}


def simulate_evaluate_testing_campaign(campaign_id: str):
    """
    Simulates evaluating the testing campaign to identify champions.
    Adds champions to the waiting queue.
    """
    if campaign_id != "creative_testing_campaign" or _MOLOCO_CAMPAIGNS[campaign_id]["status"] != "PAUSED":
        return {"error": "Testing campaign must be paused for evaluation."}

    campaign = _MOLOCO_CAMPAIGNS[campaign_id]
    control_group_id = "good_creative_group"
    
    if control_group_id not in campaign["creative_group_ids"]:
        return {"error": "Control group missing from testing campaign for evaluation."}
    
    control_performance = _MOLOCO_CREATIVE_GROUPS[control_group_id]["performance"]["conversions"]

    champions = []
    for cg_id in campaign["creative_group_ids"]:
        if cg_id == control_group_id:
            continue
        cg_performance = _MOLOCO_CREATIVE_GROUPS[cg_id]["performance"]["conversions"]
        # A simple logic for "champion": better or similar conversion rate than control
        if cg_performance >= control_performance * random.uniform(0.8, 1.2): # Allow some variability
            champions.append(cg_id)
            _MOLOCO_CHAMPION_CONCEPTS_QUEUE.append(cg_id) # Add to waiting line

    return {"message": "Evaluation complete.", "champions_identified": champions, "queue_size": len(_MOLOCO_CHAMPION_CONCEPTS_QUEUE)}

def simulate_replace_worst_creative_in_regular_campaign(campaign_id: str):
    """
    Simulates replacing the worst performing creative group in a regular campaign
    with a champion from the waiting queue.
    """
    if campaign_id not in ["regular_campaign_a", "regular_campaign_b"]:
        return {"error": "Campaign is not a regular campaign."}

    if not _MOLOCO_CHAMPION_CONCEPTS_QUEUE:
        return {"error": "No champion concepts in the waiting line."}

    campaign = _MOLOCO_CAMPAIGNS[campaign_id]
    
    # Simple logic to find the "worst" creative group (lowest conversions)
    current_cgs = [cg_id for cg_id in campaign["creative_group_ids"] if cg_id in _MOLOCO_CREATIVE_GROUPS]
    if not current_cgs:
        # If no creative groups, just add a champion
        champion_cg_id = _MOLOCO_CHAMPION_CONCEPTS_QUEUE.pop(0)
        campaign["creative_group_ids"].append(champion_cg_id)
        return {"message": f"Added champion '{champion_cg_id}' to empty regular campaign '{campaign_id}'."
                , "new_champion_id": champion_cg_id, "replaced_cg_id": None}

    worst_cg_id = None
    min_conversions = float('inf')

    for cg_id in current_cgs:
        performance = _MOLOCO_CREATIVE_GROUPS[cg_id]["performance"]
        if performance["conversions"] < min_conversions:
            min_conversions = performance["conversions"]
            worst_cg_id = cg_id
    
    if worst_cg_id:
        champion_cg_id = _MOLOCO_CHAMPION_CONCEPTS_QUEUE.pop(0)
        campaign["creative_group_ids"].remove(worst_cg_id)
        campaign["creative_group_ids"].append(champion_cg_id)
        campaign["lastModifiedTime"] = datetime.datetime.now().isoformat()
        return {"message": f"Replaced '{worst_cg_id}' with champion '{champion_cg_id}' in '{campaign_id}'."
                , "replaced_cg_id": worst_cg_id, "new_champion_id": champion_cg_id}
    else:
        return {"error": "Could not identify a 'worst' creative group to replace."}

def simulate_get_champion_queue_status():
    """Returns the current list of champion creative group IDs in the waiting queue."""
    return {"data": list(_MOLOCO_CHAMPION_CONCEPTS_QUEUE)}

# You can add more helper functions here as needed.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)