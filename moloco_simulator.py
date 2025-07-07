import uuid
import datetime
import random

# --- In-memory Data Stores (Mock Moloco Database) ---
# Each dictionary stores entities by their unique ID.

_MOLOCO_ASSETS = {} # Stores mock asset data
_MOLOCO_CREATIVES = {} # Stores mock creative data
_MOLOCO_CREATIVE_GROUPS = {} # Stores mock creative group data
_MOLOCO_CAMPAIGNS = {
    # Pre-populate required campaigns as per project specs
    "creative_testing_campaign": {
        "id": "creative_testing_campaign",
        "name": "creative_testing_campaign",
        "status": "PAUSED", # Initial status as per requirements implicitly
        "creative_group_ids": ["good_creative_group"], # Initially includes the control group
        "type": "TESTING",
        "createTime": datetime.datetime.now().isoformat(),
        "lastModifiedTime": datetime.datetime.now().isoformat(),
        "impressions_goal_per_cg": 10000 # Specific for this testing campaign
    },
    "regular_campaign_a": { # Assume two regular campaigns
        "id": "regular_campaign_a",
        "name": "regular_campaign_a",
        "status": "RUNNING",
        "creative_group_ids": [], # Initially empty, or pre-filled with mock data
        "type": "REGULAR",
        "createTime": datetime.datetime.now().isoformat(),
        "lastModifiedTime": datetime.datetime.now().isoformat(),
    },
    "regular_campaign_b": { # Assume two regular campaigns
        "id": "regular_campaign_b",
        "name": "regular_campaign_b",
        "status": "RUNNING",
        "creative_group_ids": [], # Initially empty, or pre-filled with mock data
        "type": "REGULAR",
        "createTime": datetime.datetime.now().isoformat(),
        "lastModifiedTime": datetime.datetime.now().isoformat(),
    }
}
_MOLOCO_CHAMPION_CONCEPTS_QUEUE = [] # Stores champion creative group IDs in a waiting line

# Pre-populate the "good_creative_group" as it's a control group
_MOLOCO_CREATIVE_GROUPS["good_creative_group"] = {
    "id": "good_creative_group",
    "name": "good_creative_group",
    "status": "ACTIVE",
    "creative_ids": ["creative_good_portrait", "creative_good_landscape"], # Mock creative IDs for the control group
    "createTime": datetime.datetime.now().isoformat(),
    "lastModifiedTime": datetime.datetime.now().isoformat(),
    "performance": {"conversions": 200, "impressions": 10000} # Assume it has performed well
}
_MOLOCO_CREATIVES["creative_good_portrait"] = {
    "id": "creative_good_portrait",
    "name": "good_portrait_creative",
    "creative_type": "VIDEO",
    "asset_id": "asset_good_portrait",
    "video_property": {"auto_endcard": True},
    "status": "ACTIVE",
    "createTime": datetime.datetime.now().isoformat(),
    "lastModifiedTime": datetime.datetime.now().isoformat(),
}
_MOLOCO_CREATIVES["creative_good_landscape"] = {
    "id": "creative_good_landscape",
    "name": "good_landscape_creative",
    "creative_type": "VIDEO",
    "asset_id": "asset_good_landscape",
    "video_property": {"auto_endcard": True},
    "status": "ACTIVE",
    "createTime": datetime.datetime.now().isoformat(),
    "lastModifiedTime": datetime.datetime.now().isoformat(),
}
_MOLOCO_ASSETS["asset_good_portrait"] = {
    "id": "asset_good_portrait",
    "file_name": "good_portrait_video.mp4",
    "status": "uploaded",
    "upload_time_seconds": 3,
    "createTime": datetime.datetime.now().isoformat(),
}
_MOLOCO_ASSETS["asset_good_landscape"] = {
    "id": "asset_good_landscape",
    "file_name": "good_landscape_video.mp4",
    "status": "uploaded",
    "upload_time_seconds": 3,
    "createTime": datetime.datetime.now().isoformat(),
}


# --- Helper Function for ID Generation ---
def _generate_id(prefix="id"):
    """Generates a unique ID with a given prefix."""
    return f"{prefix}_{str(uuid.uuid4()).replace('-', '_')[:8]}"

# --- Simulation Functions (Mock Moloco API Endpoints) ---

def simulate_upload_asset(file_name: str, content_type: str = "video/mp4"):
    """
    Simulates the Moloco API call to upload an asset.
    Returns a mock response dictionary.
    """
    asset_id = _generate_id("asset")
    upload_time = random.randint(2, 10) # Simulate varying upload times
    asset_data = {
        "id": asset_id,
        "file_name": file_name,
        "content_type": content_type,
        "status": "uploaded",
        "upload_time_seconds": upload_time,
        "createTime": datetime.datetime.now().isoformat(),
    }
    _MOLOCO_ASSETS[asset_id] = asset_data
    return {"data": {"id": asset_id, "status": "uploaded", "upload_time_seconds": upload_time}}

def simulate_create_creative(name: str, creative_type: str, asset_id: str, video_property: dict = None):
    """
    Simulates the Moloco API call to create a creative.
    Assumes 'VIDEO' type with auto_endcard for this project.
    Returns a mock response dictionary.
    """
    if creative_type != "VIDEO":
        return {"error": "Only VIDEO creative type is supported for this simulation."}
    if video_property is None or video_property.get("auto_endcard") is not True:
        return {"error": "VIDEO creatives must have auto_endcard=true."}

    if asset_id not in _MOLOCO_ASSETS:
        return {"error": f"Asset with ID '{asset_id}' not found."}

    creative_id = _generate_id("creative")
    creative_data = {
        "id": creative_id,
        "name": name,
        "creative_type": creative_type,
        "asset_id": asset_id,
        "video_property": video_property,
        "status": "ACTIVE", # Assume active upon creation for simplicity
        "createTime": datetime.datetime.now().isoformat(),
        "lastModifiedTime": datetime.datetime.now().isoformat(),
    }
    _MOLOCO_CREATIVES[creative_id] = creative_data
    return {"data": {"id": creative_id, "name": name, "status": "ACTIVE"}}

def simulate_create_creative_group(name: str, creative_ids: list):
    """
    Simulates the Moloco API call to create a creative group.
    Returns a mock response dictionary.
    """
    for creative_id in creative_ids:
        if creative_id not in _MOLOCO_CREATIVES:
            return {"error": f"Creative with ID '{creative_id}' not found."}

    creative_group_id = _generate_id("cg")
    creative_group_data = {
        "id": creative_group_id,
        "name": name,
        "creative_ids": creative_ids,
        "status": "ACTIVE",
        "createTime": datetime.datetime.now().isoformat(),
        "lastModifiedTime": datetime.datetime.now().isoformat(),
        "performance": {"impressions": 0, "conversions": 0} # Initialize performance metrics
    }
    _MOLOCO_CREATIVE_GROUPS[creative_group_id] = creative_group_data
    return {"data": {"id": creative_group_id, "name": name, "status": "ACTIVE"}}

def simulate_get_campaigns():
    """
    Simulates retrieving all campaign data.
    """
    campaign_list = list(_MOLOCO_CAMPAIGNS.values())
    return {"data": campaign_list}

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
        return {"message": f"Added champion '{champion_cg_id}' to empty regular campaign '{campaign_id}'."}

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
        return {"message": f"Replaced '{worst_cg_id}' with champion '{champion_cg_id}' in '{campaign_id}'."}
    else:
        return {"error": "Could not identify a 'worst' creative group to replace."}

def simulate_get_champion_queue_status():
    """Returns the current list of champion creative group IDs in the waiting queue."""
    return {"data": list(_MOLOCO_CHAMPION_CONCEPTS_QUEUE)}

# You can add more helper functions here as needed.