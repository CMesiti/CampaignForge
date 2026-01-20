## Data Structure (DTO Required?)
- No DTO Architecture for MVP1, Not required for current overall scope.

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


## Requests

### Users Endpoints
   - GET request, no parameters "/users"
      - Simple Get Request Returns users in format:
      - Content-Type application/json
      - "Data":{'Message': 'GET Successful', 
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


   - POST request, register user, required email/pass, "/users"
      // {//Invalid , No Email
      //     "password": "password123"
      // }
      // {//Invalid, No Pass
      //     "email": "user4@example.com"
      // }
      { //Valid
      "email": "user4@example.com",
      "password": "password123"
      }
      // { //Valid
      //     "email": "caseyharris@example.com",
      //     "password": "password123",
      //     "display_name": "CHarris"
      // }

   - PUT request, parameters user_id (retrieved from session) update user, required display_name or password
      - Form-Data, password or display_name



   - DELETE request, requires password, user_id (retrieved from session), delete user from db (cascade)


- Postman Request-Response Examples: 