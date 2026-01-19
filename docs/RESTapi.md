## Data Structure (DTO Required?)


{'Message': 'GET Successful', 
'Users': [{
    'user_id': UUID('f58babf1-d019-4dad-a2a5-9429783268c1'),
    'email': '-----@gmail.com', 
    'display_name': 'yoda', 
    'created_at': datetime.datetime(2026, 1, 12, 14, 52, 22, 636905), 
    'campaigns': [{
        'campaign_id': UUID('4dfdb2d5-2324-4bc4-92fb-85c5b2819ae7'), 
        'title': 'Campaign1', 
        'description': None, 
        'created_at': datetime.datetime(2026, 1, 12, 19, 46, 20, 415951), 
        'created_by': UUID('f58babf1-d019-4dad-a2a5-9429783268c1')}]}, 
    {'user_id': UUID('3f270947-4aac-41de-93a7-09530c502f15'), 
    'email': 'example@example.com', 
    'display_name': 'tester', 
    'created_at': datetime.datetime(2026, 1, 14, 19, 39, 42, 670779), 
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