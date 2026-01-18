## Data Structure (DTO Required?)

{'Message': '', 'Data': 
    [{'user_id': UUID('f58babf1-d019-4dad-a2a5-9429783268c1'), 
    'email': 'cmesiti@gmail.com', 
    'display_name': 'yoda', 
    'created_at': datetime.datetime(2026, 1, 12, 14, 52, 22, 636905), 
    'campaigns': [Campaign:
                campaign_id - 4dfdb2d5-2324-4bc4-92fb-85c5b2819ae7
                Title - Campaign1
                Description - None
                Created_By - f58babf1-d019-4dad-a2a5-9429783268c1
]}, 
    {'user_id': UUID('3f270947-4aac-41de-93a7-09530c502f15'), 'email': 'example@example.com', 'display_name': 'tester', 'created_at': datetime.datetime(2026, 1, 14, 19, 39, 42, 670779), 
    'campaigns': []}
]
}


## File Structure
- Controller (HTTP)
   ↓
- Service (business logic)
   ↓
- ORM Models (persistence)
   ↓
- DTO Mapper (representation)
   ↓
- Controller (response)

Note: 
- ORM models should describe “what exists.”
- DTOs describe “what we show.”