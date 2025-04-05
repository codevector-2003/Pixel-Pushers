
# This file contains the data for the milestones that a child should reach at a certain age.
milestones_data = [
    {"Milestone": "Smiles responsively", "Age (Months)": 1},
    {"Milestone": "Lifts head briefly while on stomach", "Age (Months)": 1},
    {"Milestone": "Follows objects with eyes", "Age (Months)": 2},
    {"Milestone": "Holds head steady while sitting", "Age (Months)": 3},
    {"Milestone": "Rolls over in both directions", "Age (Months)": 4},
    {"Milestone": "Pushes down on legs when feet are on a hard surface", "Age (Months)": 5},
    {"Milestone": "Reaches for and grasps objects", "Age (Months)": 5},
    {"Milestone": "Babbles, imitates sounds", "Age (Months)": 6},
    {"Milestone": "Sits without support", "Age (Months)": 6},
    {"Milestone": "Crawls", "Age (Months)": 7},
    {"Milestone": "Pulls to stand", "Age (Months)": 8},
    {"Milestone": "Says a few words", "Age (Months)": 9},
    {"Milestone": "Walks with support", "Age (Months)": 10},
    {"Milestone": "Walks alone", "Age (Months)": 12},
    {"Milestone": "Points at objects", "Age (Months)": 12},
    {"Milestone": "Feeds self with fingers", "Age (Months)": 12},
]


# Fetch milestones for a specific user
@app.get("/milestones/{user_id}", response_model=List[Milestone])
def get_milestones(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user["milestones"]

# Update milestone status for a specific user
@app.patch("/milestones/{user_id}/{milestone_id}")
def update_milestone(user_id: int, milestone_id: int, update: MilestoneUpdate):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    milestone = next((m for m in user["milestones"] if m["id"] == milestone_id), None)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    milestone["completed"] = update.completed
    return milestone

# Milestone model
class Milestone(BaseModel):
    challenge: str
    age: str
    title: str
    completed: bool = False  # Default to not completed